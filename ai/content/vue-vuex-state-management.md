---
id: "vue-vuex-state-management"
title: "Vue基础入门到实战6（路由进阶+面经项目）"
summary: "Vue 状态管理 Vuex 学习笔记：state、getter、mutation、action 的核心概念与模块化实践。"
canonical_url: "https://blog.fulequn.online/2024/06/Article202406141/"
published_at: "2024-06-11T07:32:22.000Z"
updated_at: "2024-06-11T07:32:22.000Z"
tags: []
---

# Vue基础入门到实战6（路由进阶+面经项目）

# 1 Vuex 概述

## 1.1 介绍

Vuex 是一个 Vue 的 状态管理工具，状态就是数据。

大白话：Vuex 是一个插件，可以帮我们管理 Vue 通用的数据 (多组件共享的数据)。例如：购物车数据 个人信息数

### 1.1.1 使用场景

-   某个状态 在 很多个组件 来使用 (个人信息)
    
-   多个组件 共同维护 一份数据 (购物车)
    

![68317818664](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247306.png)

### 1.1.2 优势

-   共同维护一份数据，**数据集中化管理**
-   **响应式变化**
-   操作简洁 (vuex 提供了一些辅助函数)

![68317829336](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247307.png)

### 1.1.3 注意

官方原文：

-   不是所有的场景都适用于 vuex，只有在必要的时候才使用 vuex
-   使用了 vuex 之后，会附加更多的框架中的概念进来，增加了项目的复杂度 （数据的操作更便捷，数据的流动更清晰）

## 1.2 vuex 的使用

![68321278417](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247308.png)

### 1.2.1 安装 vuex

安装 vuex 与 vue-router 类似，vuex 是一个独立存在的插件，如果脚手架初始化没有选 vuex，就需要额外安装。

```bash
# 233 344 vue2 对应的是 vuex3
yarn add vuex@3 或者 npm i vuex@3
```

### 1.2.2 store/index.js 专门存放 vuex

为了维护项目目录的整洁，在 src 目录下新建一个 store 目录其下放置一个 index.js 文件。 (和 `router/index.js` 类似)

​ ![68321280582](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247309.png)

### 1.2.3 创建仓库 store/index.js

```jsx
// 导入 vue
import Vue from 'vue'
// 导入 vuex
import Vuex from 'vuex'
// vuex 也是 vue 的插件, 需要 use 一下, 进行插件的安装初始化
Vue.use(Vuex)

// 创建仓库 store
const store = new Vuex.Store()
// 导出仓库
export default store
```

### 1.2.4 在 main.js 中导入挂载到 Vue 实例上

```javascript
import Vue from 'vue'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  store
}).$mount('#app')
```

此刻起, 就成功创建了一个 **空仓库!!**

### 1.2.5 测试打印 Vuex

App.vue

```javascript
created(){
  console.log(this.$store)
}
```

# 2 核心概念

## 2.1 状态 state

### 2.1.1 单一状态树

明确如何给仓库 提供 数据，如何 使用 仓库的数据

**1.提供数据**

State 提供唯一的公共数据源，所有共享的数据都要统一放到 Store 中的 State 中存储。

打开项目中的 store.js 文件，在 state 对象中可以添加我们要共享的数据。

```jsx
// 创建仓库 store
const store = new Vuex.Store({
  // state 状态, 即数据, 类似于 vue 组件中的 data,
  // 区别：
  // 1.data 是组件自己的数据, 
  // 2.state 中的数据整个 vue 项目的组件都能访问到
  state: {
    count: 101
  }
})
```

**2.访问 Vuex 中的数据**

1.  通过 $store 直接访问 —> `{{ $store.state.count }}`
2.  通过辅助函数 mapState 映射计算属性 —> `{{ count }}`

**3.通过 $store 访问的语法**

```javascript
获取 store：
 1.Vue 模板中获取 this.$store
 2.js 文件中获取 import 导入 store

模板（没有 this）中：     {{ $store.state.xxx }}
组件逻辑中：  this.$store.state.xxx
JS模块中：   store.state.xxx
```

**4.代码实现**

**模板中使用**

组件中可以使用 **$store** 获取到 vuex 中的 store 对象实例，可通过 **state** 属性属性获取 **count**， 如下

```vue
<h1>state的数据 - {{ $store.state.count }}</h1>
```

**组件逻辑中使用**

将 state 属性定义在计算属性中 [https://vuex.vuejs.org/zh/guide/state.html](https://vuex.vuejs.org/zh/guide/state.html)

```javascript
<h1>state的数据 - {{ count }}</h1>

// 把state中数据，定义在组件内的计算属性中
  computed: {
    count () {
      return this.$store.state.count
    }
  }
```

**js 文件中使用**

```javascript
//main.js

import store from "@/store"
console.log(store.state.count)
```

每次都像这样一个个的提供计算属性, 太麻烦了,我们有没有简单的语法帮我们获取state中的值呢？

### 2.1.2 辅助函数 mapState

> mapState 是辅助函数，帮助我们把 store 中的数据映射到组件的计算属性中, 它属于一种方便的用法

用法 ：

![68321471957](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247310.png)

**1.导入 mapState (mapState 是 vuex 中的一个函数)**

```javascript
import { mapState } from 'vuex'
```

**2.采用数组形式引入 state 属性**

```javascript
mapState(['count']) 
```

> 上面代码的最终得到的是 **类似于** 计算属性添加了对应的数据

```javascript
count () {
    return this.$store.state.count
}
```

**3.利用展开运算符将导出的状态映射给计算属性**

```javascript
computed: {
  ...mapState(['count'])
}
```

```vue
<div> state的数据：{{ count }}</div>
```

## 2.2 开启严格模式及 Vuex 的单向数据流

明确 vuex 同样遵循单向数据流，组件中不能直接修改仓库的数据

**直接在组件中修改Vuex中state的值**

![68321589228](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247311.png)

Son1.vue

```javascript
button @click="handleAdd">值 + 1</button>

methods:{
	 handleAdd (n) {
      // 错误代码(vue默认不会监测，监测需要成本)
       this.$store.state.count++
      // console.log(this.$store.state.count) 
    },
}
```

**开启严格模式**

通过 `strict: true` 可以开启严格模式,开启严格模式后，直接修改 state 中的值会报错

> **state 数据的修改只能通过 mutations，并且 mutations 必须是同步的**

![68321471957](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247312.png)

## 2.3 Mutation

### 2.3.1 介绍

**1.定义 mutations**

```javascript
const store  = new Vuex.Store({
  state: {
    count: 0
  },
  // 定义mutations
  mutations: {
     
  }
})
```

**2.格式说明**

mutations 是一个对象，对象中存放修改state的方法

```javascript
mutations: {
    // 方法里参数 第一个参数是当前store的state属性
    // payload 载荷 运输参数 调用mutaiions的时候 可以传递参数 传递载荷
    addCount (state) {
      state.count += 1
    }
  },
```

**3.组件中提交 mutations**

```jsx
this.$store.commit('addCount')
```

**4.总结**

通过 mutations 修改 state 的步骤

1.定义 mutations 对象，对象中存放修改 state 的方法

2.组件中提交调用 mutations(通过 $store.commit(‘mutations的方法名’))

### 2.3.2 提交载荷（Payload）

可以向 `store.commit` 传入额外的参数，即 mutation 的**载荷（payload）**

**语法**

看下面这个案例，每次点击不同的按钮，加的值都不同，每次都要定义不同的mutations处理吗？

![68321700423](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247313.png)

提交 mutation 是可以传递参数的 `this.$store.commit('xxx', 参数)`

**2.1 提供mutation函数（带参数）**

```javascript
mutations: {
  ...
  addCount (state, count) {
    state.count = count
  }
},
```

**2.2 提交mutation**

```jsx
handle ( ) {
  this.$store.commit('addCount', 10)
}
```

**小tips: 提交的参数只能是一个, 如果有多个参数要传, 可以传递一个对象**。

在大多数情况下，载荷应该是一个对象，这样可以包含多个字段并且记录的 mutation 会更易读

```jsx
this.$store.commit('addCount', {
  count: 10
}
```

### 2.3.3 mapMutations

> mapMutations 和 mapState 很像，它把位于 mutations 中的方法提取了出来，我们可以将它导入

```javascript
import  { mapMutations } from 'vuex'
methods: {
    ...mapMutations(['addCount'])
}
```

> 上面代码的含义是将 mutations 的方法导入了 methods 中，等价于

```javascript
methods: {
      // commit(方法名, 载荷参数)
      addCount () {
          this.$store.commit('addCount')
      }
 }
```

此时，就可以直接通过 this.addCount 调用了

```jsx
<button @click="addCount">值+1</button>
```

但是请注意： Vuex 中 mutations 中要求不能写异步代码，如果有异步的 ajax 请求，应该放置在 actions 中。

## 2.4 Action

> state 是存放数据的，mutations 是同步更新数据 (便于监测数据的变化, 更新视图等, 方便于调试工具查看变化)，
> 
> actions 则负责进行异步操作

**说明：mutations 必须是同步的**

**需求: 一秒钟之后，要给一个数去修改 state**

![68321860367](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247314.png)

**1.定义 actions**

```javascript
mutations: {
  changeCount (state, newCount) {
    state.count = newCount
  }
}

actions: {
  setAsyncCount (context, num) {
    // 一秒后, 给一个数, 去修改 num
    setTimeout(() => {
      context.commit('changeCount', num)
    }, 1000)
  }
},
```

**2.组件中通过 dispatch 调用**

Action 通过 `store.dispatch` 方法触发：

```javascript
store.dispatch('increment')
```

如下：

```none
setAsyncCount () {
  this.$store.dispatch('setAsyncCount', 666)
}
```

![68344198757](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247315.png)

### 2.4.1 mapActions

1.目标：掌握辅助函数 mapActions，映射方法

> mapActions 是把位于 actions 中的方法提取了出来，映射到组件 methods 中

Son2.vue

```javascript
import { mapActions } from 'vuex'
methods: {
   ...mapActions(['changeCountAction'])
}

//mapActions映射的代码 本质上是以下代码的写法
//methods: {
//  changeCountAction (n) {
//    this.$store.dispatch('changeCountAction', n)
//  },
//}
```

直接通过 this.方法 就可以调用。

```vue
<button @click="changeCountAction(200)">+异步</button>
```

## 2.5 Getter

> 除了 state 之外，有时我们还需要从 state 中**筛选出符合条件的一些数据**，这些数据是依赖 state 的，此时会用到 getters

例如，state 中定义了 list，为 1-10 的数组，

```javascript
state: {
    list: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

组件中，需要显示所有大于 5 的数据，正常的方式，是需要 list 在组件中进行再一步的处理，但是 getters 可以帮助我们实现它

### 2.5.1 定义 getters

```javascript
getters: {
   // getters 函数的第一个参数是 state
   // 必须要有返回值
   filterList: state => state.list.filter(item => item > 5)
}
```

### 2.5.2 使用 getters

**原始方式-$store**

```vue
<div>{{ $store.getters.filterList }}</div>
```

**辅助函数 - mapGetters**

```javascript
computed: {
    ...mapGetters(['filterList'])
}
```

```vue
<div>{{ filterList }}</div>
```

## 2.6 使用小结

![68344213391](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247316.png)

## 2.7 Module

由于使用 **单一状态树**，应用的所有状态 **会集中到一个比较大的对象**。当应用变得非常复杂时，store 对象就有可能变得相当臃肿。

这句话的意思是，如果把所有的状态都放在 state 中，当项目变得越来越大的时候，Vuex 会变得越来越难以维护

由此，又有了 Vuex 的模块化。

![68342575835](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247317.png)

**准备 state**

定义两个模块 **user** 和 **setting**

user中管理用户的信息状态 userInfo `modules/user.js`

```jsx
const state = {
  userInfo: {
    name: 'zs',
    age: 18
  }
}

const mutations = {}

const actions = {}

const getters = {}

export default {
  state,
  mutations,
  actions,
  getters
}
```

setting 中管理项目应用的，主题色 theme，描述 desc， `modules/setting.js`

```jsx
const state = {
  theme: 'dark'
  desc: '描述真呀真不错'
}

const mutations = {}

const actions = {}

const getters = {}

export default {
  state,
  mutations,
  actions,
  getters
}
```

在 `store/index.js` 文件中的 modules 配置项中，注册这两个模块

```javascript
import user from './modules/user'
import setting from './modules/setting'

const store = new Vuex.Store({
    modules:{
        user,
        setting
    }
})
```

使用模块中的数据, 可以直接通过模块名访问 `$store.state.模块名.xxx` => `$store.state.setting.desc`

也可以通过 mapState 映射。

# 3 项目化-获取模块内信息

## 3.1 获取模块内的 state 数据

尽管已经分模块了，但其实子模块的状态，还是会挂到根级别的 state 中，属性名就是模块名。

![68342784166](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247318.png)

**使用模块中的数据**

1.  直接通过模块名访问 `$store.state.模块名.xxx`
2.  通过 mapState 映射：
    1.  默认根级别的映射： `mapState([ 'xxx' ])`
    2.  子模块的映射：`mapState('模块名', ['xxx'])` - 需要开启命名空间 **namespaced:true**

`modules/user.js`

```jsx
const state = {
  userInfo: {
    name: 'zs',
    age: 18
  },
  myMsg: '我的数据'
}

const mutations = {
  updateMsg (state, msg) {
    state.myMsg = msg
  }
}

const actions = {}

const getters = {}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
```

**代码示例**

$store 直接访问

```javascript
$store.state.user.userInfo.name
```

mapState 辅助函数访问

```javascript
...mapState('user', ['userInfo']),
...mapState('setting', ['theme', 'desc']),
```

## 3.2 获取模块内的 getters 数据

使用模块中 getters 中的数据：

1.  直接通过模块名访问 `$store.getters['模块名/xxx ']`
2.  通过 mapGetters 映射
    1.  默认根级别的映射 `mapGetters([ 'xxx' ])`
    2.  子模块的映射 `mapGetters('模块名', ['xxx'])` - 需要开启命名空间

**代码演示**

`modules/user.js`

```javascript
const getters = {
  // 分模块后，state指代子模块的state
  UpperCaseName (state) {
    return state.userInfo.name.toUpperCase()
  }
}
```

Son1.vue 直接访问 getters

```markup
<!-- 测试访问模块中的getters - 原生 -->
<div>{{ $store.getters['user/UpperCaseName'] }}</div>
```

Son2.vue 通过命名空间访问

```javascript
computed:{
  ...mapGetters('user', ['UpperCaseName'])
}
```

## 3.3 获取模块内的 mutations 方法

默认模块中的 mutation 和 actions 会被挂载到全局，**需要开启命名空间**，才会挂载到子模块。

**调用方式**

1.  直接通过 store 调用 `$store.commit('模块名/xxx', 额外参数)`
2.  通过 mapMutations 映射
    1.  默认根级别的映射 `mapMutations([ 'xxx' ])`
    2.  子模块的映射 `mapMutations('模块名', ['xxx'])` - 需要开启命名空间

**代码实现**

`modules/user.js`

```javascript
const mutations = {
  setUser (state, newUserInfo) {
    state.userInfo = newUserInfo
  }
}
```

`modules/setting.js`

```javascript
const mutations = {
  setTheme (state, newTheme) {
    state.theme = newTheme
  }
}
```

Son1.vue

```javascript
<button @click="updateUser">更新个人信息</button> 
<button @click="updateTheme">更新主题色</button>

export default {
  methods: {
    updateUser () {
      // $store.commit('模块名/mutation名', 额外传参)
      this.$store.commit('user/setUser', {
        name: 'xiaowang',
        age: 25
      })
    }, 
    updateTheme () {
      this.$store.commit('setting/setTheme', 'pink')
    }
  }
}
```

Son2.vue

```vue
<button @click="setUser({ name: 'xiaoli', age: 80 })">更新个人信息</button>
<button @click="setTheme('skyblue')">更新主题</button>

methods:{
// 分模块的映射
...mapMutations('setting', ['setTheme']),
...mapMutations('user', ['setUser']),
}
```

## 3.4 获取模块内的 actions 方法

**注意：**

默认模块中的 mutation 和 actions 会被挂载到全局，**需要开启命名空间**，才会挂载到子模块。

**调用语法：**

1.  直接通过 store 调用 `$store.dispatch('模块名/xxx', 额外参数)`
2.  通过 mapActions 映射
    1.  默认根级别的映射 `mapActions([ 'xxx' ])`
    2.  子模块的映射 `mapActions('模块名', ['xxx'])` - 需要开启命名空间

**代码实现**

需求：

![68343161569](https://raw.githubusercontent.com/fulequn/oss_img/master/img241/202406242247319.png)

`modules/user.js`

```javascript
const actions = {
  setUserSecond (context, newUserInfo) {
    // 将异步在action中进行封装，模拟发送请求
    setTimeout(() => {
      // 调用mutation   context上下文，默认提交的就是自己模块的action和mutation
      context.commit('setUser', newUserInfo)
    }, 1000)
  }
}
```

Son1.vue 直接通过 store 调用

```vue
<button @click="updateUser2">一秒后更新信息</button>

methods:{
    updateUser2 () {
      // 调用action dispatch
      this.$store.dispatch('user/setUserSecond', {
        name: 'xiaohong',
        age: 28
      })
    },
}
```

Son2.vue mapActions 映射

```javascript
<button @click="setUserSecond({ name: 'xiaoli', age: 80 })">一秒后更新信息</button>

methods:{
  ...mapActions('user', ['setUserSecond'])
}
```

## 3.5 Vuex 模块化的使用小结

### 3.5.1 直接使用

```javascript
1. state --> $store.state.**模块名**.数据项名
2. getters --> $store.getters['**模块名**/属性名']
3. mutations --> $store.commit('**模块名**/方法名', 其他参数)
4. actions --> $store.dispatch('**模块名**/方法名', 其他参数)
```

### 3.5.2 借助辅助方法使用

```javascript
import { mapXxxx, mapXxx } from 'vuex'

computed、methods: {
    //  **...mapState、...mapGetters放computed中；**
    //  **...mapMutations、...mapActions放methods中；**
    ...mapXxxx(**'模块名'**, ['数据项|方法']),
    ...mapXxxx(**'模块名'**, {'新的名字: 原来的名字'}),
}
```

2.组件中直接使用 属性 `{{ age }}` 或 方法 `@click="updateAge(2)"`
