var searchFunc=function(t,e,n){"use strict";var i=document.getElementById(e),a=document.getElementById(n);a.innerHTML='<div class="m-auto text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div><br/>Loading...</div>',$.ajax({url:t,dataType:"xml",success:function(t){var e=$("entry",t).map(function(){return{title:$("title",this).text(),content:$("content",this).text(),url:$("url",this).text()}}).get();a.innerHTML="",i.addEventListener("input",function(){var u="",d=this.value.trim().toLowerCase().split(/[\s-]+/);if(a.innerHTML="",!(this.value.trim().length<=0)){e.forEach(function(t){var n,i,a=!0,e=(t.title&&""!==t.title.trim()||(t.title="Untitled"),t.title.trim()),s=e.toLowerCase(),l=t.content.trim().replace(/<[^>]+>/g,""),r=l.toLowerCase(),t=t.url,c=-1,o=-1;""!==r?d.forEach(function(t,e){n=s.indexOf(t),c=r.indexOf(t),n<0&&c<0?a=!1:(c<0&&(c=0),0===e&&(o=c))}):a=!1,a&&(u+="<a href='"+t+"' class='list-group-item list-group-item-action font-weight-bolder search-list-title'>"+e+"</a>",t=l,0<=o)&&(e=o+80,(e=0===(l=(l=o-20)<0?0:l)?100:e)>t.length&&(e=t.length),i=t.substring(l,e),d.forEach(function(t){var e=new RegExp(t,"gi");i=i.replace(e,'<span class="search-word">'+t+"</span>")}),u+="<p class='search-list-content'>"+i+"...</p>")});var t=$("#local-search-input");if(-1===u.indexOf("list-group-item"))return t.addClass("invalid").removeClass("valid");t.addClass("valid").removeClass("invalid"),a.innerHTML=u}})}}),$(document).on("click","#local-search-close",function(){$("#local-search-input").val("").removeClass("invalid").removeClass("valid"),$("#local-search-result").html("")})};