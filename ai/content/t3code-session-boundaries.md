---
id: "t3code-session-boundaries"
title: "T3 Code 源码学习：会话发现、进程启动与远程控制的边界"
summary: "基于固定源码版本记录会话身份、安装租约与命令回执的责任边界，区分静态源码证据、文档说明及尚未验证的恢复风险。"
canonical_url: "https://blog.fulequn.online/learn/t3code-session-boundaries/"
published_at: "2026-10-22T03:29:09.000Z"
updated_at: "2026-10-22T03:29:09.000Z"
tags: ["T3 Code","架构设计","源码学习"]
---

# T3 Code 源码学习：会话发现、进程启动与远程控制的边界

多个编码 Agent 接入同一个控制面之后，最容易混淆的并不是协议格式，而是谁负责发现会话、谁能启动进程，以及远程客户端收到的“成功”究竟确认了什么。

这篇笔记围绕这三个问题阅读 [pingdotgg/t3code](https://github.com/pingdotgg/t3code)，固定版本为 [`7d5a42912a4036549ac4c70d0195f02af432115a`](https://github.com/pingdotgg/t3code/tree/7d5a42912a4036549ac4c70d0195f02af432115a)。**本文是静态源码与文档学习，不是运行验收或安全审计：未运行该项目的测试和 demo，未核实 relay 的完整实现，也未追踪进程崩溃后的完整恢复链路。** 下文将代码观察、上游文档说明和设计推断分别标注。

## 会话发现：集成类型与配置实例分开

一种 provider 集成与一个配置实例不应混为同一个身份。`providerInstance.ts` 给出的兼容函数 `defaultInstanceIdForDriver`，仍以 driver kind 构造默认 instance id。注释说明，旧版本每种 driver 只有一个 instance；保留这个映射，是为了让已持久化的线程、绑定和缓存继续可路由，而不必改写它们保存的选择信息（[E7](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/packages/contracts/src/providerInstance.ts#L160-L168)）。这是类型分离后仍需承担存储兼容成本的一个具体例子，不能据此推断全部迁移路径已经得到验证。

另一个边界是健康检查与已认证会话的数据来源。Antigravity provider 的注释明确写着：健康检查使用 `initialize`，账户级元数据由 session 回调提供，禁用的 instance 不展示这些信息（[E5](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/provider/AntigravityProvider.ts#L135-L203)）。这支持“探测与认证会话分开设计”的判断；它不证明健康检查完全没有进程、网络或文件副作用，因此不能简单概括成“探测零副作用”。

线程身份还影响 MCP 凭证的准备过程。`ProviderSessionManager` 用 `threadId + mcpCredentialId` 构造 reservation key，并通过线程级锁串行化凭证准备。注释指出，凭证从准备函数交出、到 session entry 被登记之间存在一个窗口，reservation 用来避免此时被竞争释放的操作撤销（[E8](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/orchestration-v2/ProviderSessionManager.ts#L435-L472)）。这里核实的是生命周期保护机制，不是“所有跨线程凭证访问都已被安全审计”的结论。

## 进程启动：安装版本与使用版本的生命周期分开

`AntigravityInstallation` 将 `releaseId` 限定为 64 位十六进制字符串；active release 保存的是一个独立的 release id 指针。`acquire` 的接口注释要求：持有 lease，直到启动的子进程退出（[E6](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/provider/AntigravityInstallation.ts#L46-L90)）。

这是一项值得借鉴的接口约束：客户端连接可以断开，使用中的安装版本却仍需由进程生命周期保护。安装器不能仅因为某个连接结束，就认定对应版本已经无人使用。本文没有对升级、删除及异常退出做运行测试，所以只将“lease 应覆盖子进程生命周期”作为已读到的契约，不写成“运行中的进程绝不会被升级影响”。

## 远程控制：命令回执与效果完成分开

在客户端与 server 的 RPC 契约中，`WsRpcGroup` 汇总了 WebSocket RPC。`RpcScopeAuthorization` 的注释说明，连接的 scope 在 handler 运行前与 RPC 声明的 scope 比较，组内每个 RPC 都携带这项中间件（[E1](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/packages/contracts/src/rpc.ts#L1868-L1885)）。这是把授权要求放在公共契约层的设计证据；它不等于对所有其他入口或运行时实现作出安全保证。

更值得注意的是回执的含义。`EventSink` 的 `commitProjectCommand` 接口把项目事件、投影更新和命令回执放在同一个事务中。实现先尝试保留 command id，已有回执时直接返回；新命令才追加事件、更新投影并写回执（[E2](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/orchestration-v2/EventSink.ts#L681-L706)）。这能避免同一个 command id 重复提交项目事件，但不能替后续外部效果承诺“只执行一次”。

外部效果由独立 worker 领取。`EffectWorker` 调用 `outbox.claimNext({ workerId, leaseDurationMs, ... })` 取得工作（[E3](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/orchestration-v2/EffectWorker.ts#L689-L706)）；执行结束后调用 `outbox.succeed`，无法确认 lease 所有权时返回错误（[E4](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/apps/server/src/orchestration-v2/EffectWorker.ts#L739-L760)）。

这个顺序有一个重要限制：效果可能已经执行，随后才发现完成状态无法结算。上述片段证明了完成结算时的所有权检查，并不证明 lease 丢失会立即停止已经发出的外部操作，也不保证所有效果都可以安全重放。本文未追踪 `RestartContinuation` 的完整恢复逻辑，不能把 outbox 加 lease 等同于端到端的“恰好一次执行”。

因此，收到命令回执时，能确认的是“意图已提交”；provider 工作、CI 或部署是否完成，还需要各自的结果证据。

## 远程路由与 relay：文档说明仍需实现验证

上游远程访问文档把环境身份与访问路由分开描述，并说明 learned route 复用发现它的那条路由的凭证，使用之前仍需确认回应者是预期 environment（[E10](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/docs/internals/remote.md)）。这些是本次读到的文档设计，不是已完成的跨路由运行测试。

T3 Connect 文档将 relay 称为 trusted broker：relay 请求 environment 铸造绑定客户端 DPoP key 的一次性 bootstrap 凭证，客户端再直接与 environment 交换访问凭证；应用流量通过 environment 的 tunnel hostname 传输，而不是由 relay Worker 代理 HTTP 或 WebSocket 会话（[E9](https://github.com/pingdotgg/t3code/blob/7d5a42912a4036549ac4c70d0195f02af432115a/docs/internals/t3-connect.md)）。“relay 自己铸造全部凭证”不是这段文档的准确表述。

同一文档也写明了信任假设：relay 持有 mint 请求的签名权，DPoP 防止诚实交换中的凭证复用，却不能使已经泄露的 relay 签名密钥变得无害。个人单机场景如果没有对应的云信任边界，不应只复制流程图中的组件名称。这里的判断仍以文档为依据，relay 凭证铸造与校验的完整代码路径留待后续核实。

## 可以迁移的设计，以及不能直接照搬的保证

本次最有用的设计模式是：**先持久化命令意图与回执，再由独立执行者推进效果；命令确认与效果验收使用不同证据。** 它适用于写操作确认后仍可能失败、而失败又不能直接重试的系统，例如源码归档、迁移或发布流程。

借鉴时至少需要保留三个条件：意图有持久化记录；执行者有 lease 或等价所有权；恢复能判断外部效果当前状态，并区分可重放、不可重放和结果未知。本文核实了前两类机制中的部分代码，第三项只追踪到领取与结算片段，完整恢复策略仍待验证。这些条件是采用该模式时的设计要求，不是对 T3 Code 所有效果类型已经满足它们的保证。

对 `github-trending-tracker` 而言，可借鉴的是探测与 setup 的职责拆分，以及“确认记录不代表外部操作完成”的状态语义。多 provider instance 的归一化暂时没有直接需求；relay 与云身份体系也不宜因上游采用了它们，就成为个人单机工具的默认组件。单进程、无持久化要求的小工具，更没有必要为形式上的一致性引入完整 outbox。

## 本次学习的证据边界

-   **源码观察**：RPC scope 中间件的契约说明；项目命令回执与事件提交；效果领取与完成结算；Antigravity 探测的数据来源；安装 lease 的接口约束；instance 兼容映射；MCP 凭证准备的 reservation 与线程锁。
-   **文档说明**：远程路由、bootstrap 交换与 relay 的信任假设。未将其记作已核实的完整实现。
-   **设计推断**：适配成本不仅在协议格式，还在身份、权限和会话生命周期的归一化；持久化意图与独立效果执行对 tracker 的归档和发布流程有借鉴价值。
-   **未完成验证**：上游测试与 demo、真实远程连接、relay 铸造及 DPoP 校验全链路、进程崩溃后的效果重放与退役策略。

后续阅读应沿着 relay 的 bootstrap 代码与 `RestartContinuation` 恢复链继续，而不是把本次静态学习中的接口约束当成运行验收结论。
