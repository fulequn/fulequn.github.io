!function(t,n){var o=n.documentElement,a="Fluid_Color_Scheme",e="--color-mode",l="data-user-color-scheme",r="data-default-color-scheme",c="color-toggle-icon";function i(t){try{return localStorage.getItem(t)}catch(t){return null}}function u(){var t=getComputedStyle(o).getPropertyValue(e);return"string"==typeof t?t.replace(/["'\s]/g,""):null}function d(){o.setAttribute(l,s());var t=a;try{localStorage.removeItem(t)}catch(t){}}var g={dark:!0,light:!0};function s(){var t="string"==typeof(t=o.getAttribute(r))?t.replace(/["'\s]/g,""):null;return g[t]||(t=u(),g[t])?t:18<=(t=(new Date).getHours())||0<=t&&t<=6?"dark":"light"}function f(t){var e,t=t||i(a)||s();if(t===s())d();else{if(!g[t])return void d();o.setAttribute(l,t)}var r=t;g[r]&&(e="icon-dark",r&&(e="icon-"+m[r]),(t=n.getElementById(c))?(t.setAttribute("class","iconfont "+e),t.setAttribute("data",m[r])):waitElementLoaded(c,function(){var t=n.getElementById(c);t&&(t.setAttribute("class","iconfont "+e),t.setAttribute("data",m[r]))}))}var m={dark:"light",light:"dark"};function v(){var t=i(a);if(g[t])t=m[t];else{if(null!==t)return;var e=n.getElementById(c);e&&(t=e.getAttribute("data")),e&&g[t]||(t=m[u()])}var e=a,r=t;try{localStorage.setItem(e,r)}catch(t){}return t}f();var y=t.onload;t.onload=function(){y&&y(),n.getElementById("color-toggle-btn").addEventListener("click",()=>{f(v())})}}(window,document);