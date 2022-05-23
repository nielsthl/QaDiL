/*!***************************************************
* mark.js v8.11.1
* https://markjs.io/
* Copyright (c) 2014–2018, Julian Kühnel
* Released under the MIT license https://git.io/vwTVl */
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?module.exports=t():"function"==typeof define&&define.amd?define(t):e.Mark=t()}(this,function(){"use strict";var e="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},t=function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")},n=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),r=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},i=function(){function e(n){var r=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],i=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],o=arguments.length>3&&void 0!==arguments[3]?arguments[3]:5e3;t(this,e),this.ctx=n,this.iframes=r,this.exclude=i,this.iframesTimeout=o}return n(e,[{key:"getContexts",value:function(){var e=[];return(void 0!==this.ctx&&this.ctx?NodeList.prototype.isPrototypeOf(this.ctx)?Array.prototype.slice.call(this.ctx):Array.isArray(this.ctx)?this.ctx:"string"==typeof this.ctx?Array.prototype.slice.call(document.querySelectorAll(this.ctx)):[this.ctx]:[]).forEach(function(t){var n=e.filter(function(e){return e.contains(t)}).length>0;-1!==e.indexOf(t)||n||e.push(t)}),e}},{key:"getIframeContents",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:function(){},r=void 0;try{var i=e.contentWindow;if(r=i.document,!i||!r)throw new Error("iframe inaccessible")}catch(e){n()}r&&t(r)}},{key:"isIframeBlank",value:function(e){var t=e.getAttribute("src").trim();return"about:blank"===e.contentWindow.location.href&&"about:blank"!==t&&t}},{key:"observeIframeLoad",value:function(e,t,n){var r=this,i=!1,o=null,a=function a(){if(!i){i=!0,clearTimeout(o);try{r.isIframeBlank(e)||(e.removeEventListener("load",a),r.getIframeContents(e,t,n))}catch(e){n()}}};e.addEventListener("load",a),o=setTimeout(a,this.iframesTimeout)}},{key:"onIframeReady",value:function(e,t,n){try{"complete"===e.contentWindow.document.readyState?this.isIframeBlank(e)?this.observeIframeLoad(e,t,n):this.getIframeContents(e,t,n):this.observeIframeLoad(e,t,n)}catch(e){n()}}},{key:"waitForIframes",value:function(e,t){var n=this,r=0;this.forEachIframe(e,function(){return!0},function(e){r++,n.waitForIframes(e.querySelector("html"),function(){--r||t()})},function(e){e||t()})}},{key:"forEachIframe",value:function(t,n,r){var i=this,o=arguments.length>3&&void 0!==arguments[3]?arguments[3]:function(){},a=t.querySelectorAll("iframe"),s=a.length,c=0;a=Array.prototype.slice.call(a);var u=function(){--s<=0&&o(c)};s||u(),a.forEach(function(t){e.matches(t,i.exclude)?u():i.onIframeReady(t,function(e){n(t)&&(c++,r(e)),u()},u)})}},{key:"createIterator",value:function(e,t,n){return document.createNodeIterator(e,t,n,!1)}},{key:"createInstanceOnIframe",value:function(t){return new e(t.querySelector("html"),this.iframes)}},{key:"compareNodeIframe",value:function(e,t,n){if(e.compareDocumentPosition(n)&Node.DOCUMENT_POSITION_PRECEDING){if(null===t)return!0;if(t.compareDocumentPosition(n)&Node.DOCUMENT_POSITION_FOLLOWING)return!0}return!1}},{key:"getIteratorNode",value:function(e){var t=e.previousNode();return{prevNode:t,node:null===t?e.nextNode():e.nextNode()&&e.nextNode()}}},{key:"checkIframeFilter",value:function(e,t,n,r){var i=!1,o=!1;return r.forEach(function(e,t){e.val===n&&(i=t,o=e.handled)}),this.compareNodeIframe(e,t,n)?(!1!==i||o?!1===i||o||(r[i].handled=!0):r.push({val:n,handled:!0}),!0):(!1===i&&r.push({val:n,handled:!1}),!1)}},{key:"handleOpenIframes",value:function(e,t,n,r){var i=this;e.forEach(function(e){e.handled||i.getIframeContents(e.val,function(e){i.createInstanceOnIframe(e).forEachNode(t,n,r)})})}},{key:"iterateThroughNodes",value:function(e,t,n,r,i){for(var o,a=this,s=this.createIterator(t,e,r),c=[],u=[],l=void 0,h=void 0;void 0,o=a.getIteratorNode(s),h=o.prevNode,l=o.node;)this.iframes&&this.forEachIframe(t,function(e){return a.checkIframeFilter(l,h,e,c)},function(t){a.createInstanceOnIframe(t).forEachNode(e,function(e){return u.push(e)},r)}),u.push(l);u.forEach(function(e){n(e)}),this.iframes&&this.handleOpenIframes(c,e,n,r),i()}},{key:"forEachNode",value:function(e,t,n){var r=this,i=arguments.length>3&&void 0!==arguments[3]?arguments[3]:function(){},o=this.getContexts(),a=o.length;a||i(),o.forEach(function(o){var s=function(){r.iterateThroughNodes(e,o,t,n,function(){--a<=0&&i()})};r.iframes?r.waitForIframes(o,s):s()})}}],[{key:"matches",value:function(e,t){var n="string"==typeof t?[t]:t,r=e.matches||e.matchesSelector||e.msMatchesSelector||e.mozMatchesSelector||e.oMatchesSelector||e.webkitMatchesSelector;if(r){var i=!1;return n.every(function(t){return!r.call(e,t)||(i=!0,!1)}),i}return!1}}]),e}(),o=function(){function o(e){t(this,o),this.ctx=e,this.ie=!1;var n=window.navigator.userAgent;(n.indexOf("MSIE")>-1||n.indexOf("Trident")>-1)&&(this.ie=!0)}return n(o,[{key:"log",value:function(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"debug",r=this.opt.log;this.opt.debug&&"object"===(void 0===r?"undefined":e(r))&&"function"==typeof r[n]&&r[n]("mark.js: "+t)}},{key:"escapeStr",value:function(e){return e.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g,"\\$&")}},{key:"createRegExp",value:function(e){return"disabled"!==this.opt.wildcards&&(e=this.setupWildcardsRegExp(e)),e=this.escapeStr(e),Object.keys(this.opt.synonyms).length&&(e=this.createSynonymsRegExp(e)),(this.opt.ignoreJoiners||this.opt.ignorePunctuation.length)&&(e=this.setupIgnoreJoinersRegExp(e)),this.opt.diacritics&&(e=this.createDiacriticsRegExp(e)),e=this.createMergedBlanksRegExp(e),(this.opt.ignoreJoiners||this.opt.ignorePunctuation.length)&&(e=this.createJoinersRegExp(e)),"disabled"!==this.opt.wildcards&&(e=this.createWildcardsRegExp(e)),e=this.createAccuracyRegExp(e)}},{key:"createSynonymsRegExp",value:function(e){var t=this.opt.synonyms,n=this.opt.caseSensitive?"":"i",r=this.opt.ignoreJoiners||this.opt.ignorePunctuation.length?"\0":"";for(var i in t)if(t.hasOwnProperty(i)){var o=t[i],a="disabled"!==this.opt.wildcards?this.setupWildcardsRegExp(i):this.escapeStr(i),s="disabled"!==this.opt.wildcards?this.setupWildcardsRegExp(o):this.escapeStr(o);""!==a&&""!==s&&(e=e.replace(new RegExp("("+this.escapeStr(a)+"|"+this.escapeStr(s)+")","gm"+n),r+"("+this.processSynomyms(a)+"|"+this.processSynomyms(s)+")"+r))}return e}},{key:"processSynomyms",value:function(e){return(this.opt.ignoreJoiners||this.opt.ignorePunctuation.length)&&(e=this.setupIgnoreJoinersRegExp(e)),e}},{key:"setupWildcardsRegExp",value:function(e){return(e=e.replace(/(?:\\)*\?/g,function(e){return"\\"===e.charAt(0)?"?":""})).replace(/(?:\\)*\*/g,function(e){return"\\"===e.charAt(0)?"*":""})}},{key:"createWildcardsRegExp",value:function(e){var t="withSpaces"===this.opt.wildcards;return e.replace(/\u0001/g,t?"[\\S\\s]?":"\\S?").replace(/\u0002/g,t?"[\\S\\s]*?":"\\S*")}},{key:"setupIgnoreJoinersRegExp",value:function(e){return e.replace(/[^(|)\\]/g,function(e,t,n){var r=n.charAt(t+1);return/[(|)\\]/.test(r)||""===r?e:e+"\0"})}},{key:"createJoinersRegExp",value:function(e){var t=[],n=this.opt.ignorePunctuation;return Array.isArray(n)&&n.length&&t.push(this.escapeStr(n.join(""))),this.opt.ignoreJoiners&&t.push("\\u00ad\\u200b\\u200c\\u200d"),t.length?e.split(/\u0000+/).join("["+t.join("")+"]*"):e}},{key:"createDiacriticsRegExp",value:function(e){var t=this.opt.caseSensitive?"":"i",n=this.opt.caseSensitive?["aàáảãạăằắẳẵặâầấẩẫậäåāą","AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÄÅĀĄ","cçćč","CÇĆČ","dđď","DĐĎ","eèéẻẽẹêềếểễệëěēę","EÈÉẺẼẸÊỀẾỂỄỆËĚĒĘ","iìíỉĩịîïī","IÌÍỈĨỊÎÏĪ","lł","LŁ","nñňń","NÑŇŃ","oòóỏõọôồốổỗộơởỡớờợöøō","OÒÓỎÕỌÔỒỐỔỖỘƠỞỠỚỜỢÖØŌ","rř","RŘ","sšśșş","SŠŚȘŞ","tťțţ","TŤȚŢ","uùúủũụưừứửữựûüůū","UÙÚỦŨỤƯỪỨỬỮỰÛÜŮŪ","yýỳỷỹỵÿ","YÝỲỶỸỴŸ","zžżź","ZŽŻŹ"]:["aàáảãạăằắẳẵặâầấẩẫậäåāąAÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÄÅĀĄ","cçćčCÇĆČ","dđďDĐĎ","eèéẻẽẹêềếểễệëěēęEÈÉẺẼẸÊỀẾỂỄỆËĚĒĘ","iìíỉĩịîïīIÌÍỈĨỊÎÏĪ","lłLŁ","nñňńNÑŇŃ","oòóỏõọôồốổỗộơởỡớờợöøōOÒÓỎÕỌÔỒỐỔỖỘƠỞỠỚỜỢÖØŌ","rřRŘ","sšśșşSŠŚȘŞ","tťțţTŤȚŢ","uùúủũụưừứửữựûüůūUÙÚỦŨỤƯỪỨỬỮỰÛÜŮŪ","yýỳỷỹỵÿYÝỲỶỸỴŸ","zžżźZŽŻŹ"],r=[];return e.split("").forEach(function(i){n.every(function(n){if(-1!==n.indexOf(i)){if(r.indexOf(n)>-1)return!1;e=e.replace(new RegExp("["+n+"]","gm"+t),"["+n+"]"),r.push(n)}return!0})}),e}},{key:"createMergedBlanksRegExp",value:function(e){return e.replace(/[\s]+/gim,"[\\s]+")}},{key:"createAccuracyRegExp",value:function(e){var t=this,n=this.opt.accuracy,r="string"==typeof n?n:n.value,i="";switch(("string"==typeof n?[]:n.limiters).forEach(function(e){i+="|"+t.escapeStr(e)}),r){case"partially":default:return"()("+e+")";case"complementary":return"()([^"+(i="\\s"+(i||this.escapeStr("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¡¿")))+"]*"+e+"[^"+i+"]*)";case"exactly":return"(^|\\s"+i+")("+e+")(?=$|\\s"+i+")"}}},{key:"getSeparatedKeywords",value:function(e){var t=this,n=[];return e.forEach(function(e){t.opt.separateWordSearch?e.split(" ").forEach(function(e){e.trim()&&-1===n.indexOf(e)&&n.push(e)}):e.trim()&&-1===n.indexOf(e)&&n.push(e)}),{keywords:n.sort(function(e,t){return t.length-e.length}),length:n.length}}},{key:"isNumeric",value:function(e){return Number(parseFloat(e))==e}},{key:"checkRanges",value:function(e){var t=this;if(!Array.isArray(e)||"[object Object]"!==Object.prototype.toString.call(e[0]))return this.log("markRanges() will only accept an array of objects"),this.opt.noMatch(e),[];var n=[],r=0;return e.sort(function(e,t){return e.start-t.start}).forEach(function(e){var i=t.callNoMatchOnInvalidRanges(e,r),o=i.start,a=i.end;i.valid&&(e.start=o,e.length=a-o,n.push(e),r=a)}),n}},{key:"callNoMatchOnInvalidRanges",value:function(e,t){var n=void 0,r=void 0,i=!1;return e&&void 0!==e.start?(r=(n=parseInt(e.start,10))+parseInt(e.length,10),this.isNumeric(e.start)&&this.isNumeric(e.length)&&r-t>0&&r-n>0?i=!0:(this.log("Ignoring invalid or overlapping range: "+JSON.stringify(e)),this.opt.noMatch(e))):(this.log("Ignoring invalid range: "+JSON.stringify(e)),this.opt.noMatch(e)),{start:n,end:r,valid:i}}},{key:"checkWhitespaceRanges",value:function(e,t,n){var r=void 0,i=!0,o=n.length,a=t-o,s=parseInt(e.start,10)-a;return(r=(s=s>o?o:s)+parseInt(e.length,10))>o&&(r=o,this.log("End range automatically set to the max value of "+o)),s<0||r-s<0||s>o||r>o?(i=!1,this.log("Invalid range: "+JSON.stringify(e)),this.opt.noMatch(e)):""===n.substring(s,r).replace(/\s+/g,"")&&(i=!1,this.log("Skipping whitespace only range: "+JSON.stringify(e)),this.opt.noMatch(e)),{start:s,end:r,valid:i}}},{key:"getTextNodes",value:function(e){var t=this,n="",r=[];this.iterator.forEachNode(NodeFilter.SHOW_TEXT,function(e){r.push({start:n.length,end:(n+=e.textContent).length,node:e})},function(e){return t.matchesExclude(e.parentNode)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT},function(){e({value:n,nodes:r})})}},{key:"matchesExclude",value:function(e){return i.matches(e,this.opt.exclude.concat(["script","style","title","head","html"]))}},{key:"wrapRangeInTextNode",value:function(e,t,n){var r=this.opt.element?this.opt.element:"mark",i=e.splitText(t),o=i.splitText(n-t),a=document.createElement(r);return a.setAttribute("data-markjs","true"),this.opt.className&&a.setAttribute("class",this.opt.className),a.textContent=i.textContent,i.parentNode.replaceChild(a,i),o}},{key:"wrapRangeInMappedTextNode",value:function(e,t,n,r,i){var o=this;e.nodes.every(function(a,s){var c=e.nodes[s+1];if(void 0===c||c.start>t){if(!r(a.node))return!1;var u=t-a.start,l=(n>a.end?a.end:n)-a.start,h=e.value.substr(0,a.start),f=e.value.substr(l+a.start);if(a.node=o.wrapRangeInTextNode(a.node,u,l),e.value=h+f,e.nodes.forEach(function(t,n){n>=s&&(e.nodes[n].start>0&&n!==s&&(e.nodes[n].start-=l),e.nodes[n].end-=l)}),n-=l,i(a.node.previousSibling,a.start),!(n>a.end))return!1;t=a.end}return!0})}},{key:"wrapMatches",value:function(e,t,n,r,i){var o=this,a=0===t?0:t+1;this.getTextNodes(function(t){t.nodes.forEach(function(t){t=t.node;for(var i=void 0;null!==(i=e.exec(t.textContent))&&""!==i[a];)if(n(i[a],t)){var s=i.index;if(0!==a)for(var c=1;c<a;c++)s+=i[c].length;t=o.wrapRangeInTextNode(t,s,s+i[a].length),r(t.previousSibling),e.lastIndex=0}}),i()})}},{key:"wrapMatchesAcrossElements",value:function(e,t,n,r,i){var o=this,a=0===t?0:t+1;this.getTextNodes(function(t){for(var s=void 0;null!==(s=e.exec(t.value))&&""!==s[a];){var c=s.index;if(0!==a)for(var u=1;u<a;u++)c+=s[u].length;var l=c+s[a].length;o.wrapRangeInMappedTextNode(t,c,l,function(e){return n(s[a],e)},function(t,n){e.lastIndex=n,r(t)})}i()})}},{key:"wrapRangeFromIndex",value:function(e,t,n,r){var i=this;this.getTextNodes(function(o){var a=o.value.length;e.forEach(function(e,r){var s=i.checkWhitespaceRanges(e,a,o.value),c=s.start,u=s.end;s.valid&&i.wrapRangeInMappedTextNode(o,c,u,function(n){return t(n,e,o.value.substring(c,u),r)},function(t){n(t,e)})}),r()})}},{key:"unwrapMatches",value:function(e){for(var t=e.parentNode,n=document.createDocumentFragment();e.firstChild;)n.appendChild(e.removeChild(e.firstChild));t.replaceChild(n,e),this.ie?this.normalizeTextNode(t):t.normalize()}},{key:"normalizeTextNode",value:function(e){if(e){if(3===e.nodeType)for(;e.nextSibling&&3===e.nextSibling.nodeType;)e.nodeValue+=e.nextSibling.nodeValue,e.parentNode.removeChild(e.nextSibling);else this.normalizeTextNode(e.firstChild);this.normalizeTextNode(e.nextSibling)}}},{key:"markRegExp",value:function(e,t){var n=this;this.opt=t,this.log('Searching with expression "'+e+'"');var r=0,i="wrapMatches";this.opt.acrossElements&&(i="wrapMatchesAcrossElements"),this[i](e,this.opt.ignoreGroups,function(e,t){return n.opt.filter(t,e,r)},function(e){r++,n.opt.each(e)},function(){0===r&&n.opt.noMatch(e),n.opt.done(r)})}},{key:"mark",value:function(e,t){var n=this;this.opt=t;var r=0,i="wrapMatches",o=this.getSeparatedKeywords("string"==typeof e?[e]:e),a=o.keywords,s=o.length,c=this.opt.caseSensitive?"":"i";this.opt.acrossElements&&(i="wrapMatchesAcrossElements"),0===s?this.opt.done(r):function e(t){var o=new RegExp(n.createRegExp(t),"gm"+c),u=0;n.log('Searching with expression "'+o+'"'),n[i](o,1,function(e,i){return n.opt.filter(i,t,r,u)},function(e){u++,r++,n.opt.each(e)},function(){0===u&&n.opt.noMatch(t),a[s-1]===t?n.opt.done(r):e(a[a.indexOf(t)+1])})}(a[0])}},{key:"markRanges",value:function(e,t){var n=this;this.opt=t;var r=0,i=this.checkRanges(e);i&&i.length?(this.log("Starting to mark with the following ranges: "+JSON.stringify(i)),this.wrapRangeFromIndex(i,function(e,t,r,i){return n.opt.filter(e,t,r,i)},function(e,t){r++,n.opt.each(e,t)},function(){n.opt.done(r)})):this.opt.done(r)}},{key:"unmark",value:function(e){var t=this;this.opt=e;var n=this.opt.element?this.opt.element:"*";n+="[data-markjs]",this.opt.className&&(n+="."+this.opt.className),this.log('Removal selector "'+n+'"'),this.iterator.forEachNode(NodeFilter.SHOW_ELEMENT,function(e){t.unwrapMatches(e)},function(e){var r=i.matches(e,n),o=t.matchesExclude(e);return!r||o?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT},this.opt.done)}},{key:"opt",set:function(e){this._opt=r({},{element:"",className:"",exclude:[],iframes:!1,iframesTimeout:5e3,separateWordSearch:!0,diacritics:!0,synonyms:{},accuracy:"partially",acrossElements:!1,caseSensitive:!1,ignoreJoiners:!1,ignoreGroups:0,ignorePunctuation:[],wildcards:"disabled",each:function(){},noMatch:function(){},filter:function(){return!0},done:function(){},debug:!1,log:window.console},e)},get:function(){return this._opt}},{key:"iterator",get:function(){return new i(this.ctx,this.opt.iframes,this.opt.exclude,this.opt.iframesTimeout)}}]),o}();return function(e){var t=this,n=new o(e);return this.mark=function(e,r){return n.mark(e,r),t},this.markRegExp=function(e,r){return n.markRegExp(e,r),t},this.markRanges=function(e,r){return n.markRanges(e,r),t},this.unmark=function(e){return n.unmark(e),t},this}});
/****************************************************!*/

var searchHasBeenInit = false;
var searchSupportedChars = /[a-z0-9\-\.æøå ]/;
var searchDict = new Map();
var searchFilesNumLoaded = 0;
var searchFilesRaw = {};
var searchFilesTransformed = {};
var searchFilenames = []; /* this variable gets populated in the searchDomReady function */
var searchLocalStorageKey = 'QaDiLSearchData';
var searchLocalStorageExpires = 604800000; /* 1 week in milliseconds */

function searchGetInternalStateJSON() {
    var data = {
        timeStamp              : new Date().getTime(),
        searchDict             : Array.from(searchDict.entries()),
        searchFilesTransformed : searchFilesTransformed
    };

    return JSON.stringify(data);
}

function searchSetInternalStateFromLocalStorage() {
    var data = JSON.parse(window.localStorage.getItem(searchLocalStorageKey));
    
    searchDict = new Map(data.searchDict);
    searchFilesTransformed = data.searchFilesTransformed;
    searchHasBeenInit = true;
}

function searchShouldScrapeForData() {
    var data = window.localStorage.getItem(searchLocalStorageKey);
    
    if (data === null)
        return true;

    var parsedData = JSON.parse(data);
    return (new Date().getTime() - parsedData.timeStamp >= searchLocalStorageExpires);
}

function searchLoadFiles(finishedCallback) {
    searchFilenames.forEach(function(file) {
        function listener() {
            searchFilesRaw[file] = this.responseText;
            searchFilesNumLoaded++;
            
            if (searchFilesNumLoaded == searchFilenames.length) {
                finishedCallback();
            }
        }

        var request = new XMLHttpRequest();
        request.addEventListener('load', listener);
        request.open('GET', file + '.html', true);
        request.send();
    });
}

function searchTransformFile(file) {
    // get rid of everything before the actual article starts
    file = file.substring(file.indexOf('<div class="main'));

    // get rid of unnecessary whitespace
    file = file.replace(/\s+/g, ' ');

    // makes a RegExp which matches <tag (attributes)>(content)</tag>
    function makeTagReg(tag) {
        return RegExp('<' + tag + '(.*?)>(.*?)<\/' + tag + '>');
    }

    // transform specific tags by only keeping their inner content
    var transformTags = ['b', 'h1', 'h2', 'h3', 'a', 'div', 'span', 'figcaption', 'em', 'ol', 'ul', 'li'];

    for (var tag of transformTags) {
        var tagReg = makeTagReg(tag);
        while (tagReg.test(file)) {
            var match = file.match(tagReg);
            var newContent = ' ' + match[2] + ' ';

            // specific rule for h1, h2, h3
            if (tag.charAt(0) == 'h') {
                newContent = '\n\n' + newContent + '\n';
            }

            file = file.replace(match[0], newContent);
        }
    }

    // completely remove specific tags and their content
    var removeTags = ['script', 'iframe'];

    for (var tag of removeTags) {
        var tagReg = makeTagReg(tag);
        while (tagReg.test(file)) {
            var match = file.match(tagReg);
            file = file.replace(match[0], ' ');
        }
    }

    // remove any leftover HTML
    var tagReg = /<(.*?)>|<\/(.*?)>/;
    while (tagReg.test(file)) {
        var match = file.match(tagReg);
        file = file.replace(match[0], '');
    }

    // get rid of unnecessary whitespace again but this time keep newlines
    file = file.replace(/[^\S\r\n]+/g, ' ');

    // get rid of extra spaces after newlines
    file = file.replace(/\n( )+/g, '\n');

    // completely remove whitespace from start and end
    file = file.replace(/^\s+|\s+$/g, '');

    var sections = file.split(/\n\n+/g)
                       .map(section => section.split(/\s*\n\s*/));

    // convert content to lower case and remove redundant characters
    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];

        if (section.length > 1) {
            section[1] = searchConvertString(section[1]);
        }
    }

    // populate dictionary with words from this chapter
    for (var section of sections) {
        var [header, content] = section;
        
        searchAddWordsToDict(header);

        if (section.length > 1)
            searchAddWordsToDict(content);
    }

    return sections;
}

function searchAddWordsToDict(str) {
    // str = searchConvertString(str.replace(/^\s+|\s+$/g, ''));
    str = searchConvertString(str);

    var words = str.split(' ');

    for (var word of words) {
        if (!searchDict.has(word)) {
            searchDict.set(word, 0);
        }

        searchDict.set(word, searchDict.get(word) + 1);
    }
}

function searchConvertString(str) {
    return str.replace(/^\s+|\s+$/g, '')
              .toLowerCase()
              .split('')
              .filter(ch => searchSupportedChars.test(ch))
              .join('')
              .replace(/\s+|\-/g, ' ')
              .split(/\s+/g)
              .map(word => word.replace(/\.$/, ''))
              .join(' ');
}

function searchComputeEditDistance(s, t) {
    // DP solution from https://en.wikipedia.org/wiki/Levenshtein_distance#Iterative_with_full_matrix
    
    var i, j;
    var m = s.length;
    var n = t.length;
    var d = [];

    for (i = 0; i <= m; i++) {
        d.push([]);
        for (j = 0; j <= n; j++) {
            d[i][j] = 0;
        }
    }

    for (i = 1; i <= m; i++)
        d[i][0] = i;

    for (j = 1; j <= n; j++)
        d[0][j] = j;

    for (j = 1; j <= n; j++) {
        for (i = 1; i <= m; i++) {
            var substitutionCost;

            if (s.charAt(i - 1) == t.charAt(j - 1))
                substitutionCost = 0;
            else
                substitutionCost = 1;

            d[i][j] = Math.min(
                Math.min(
                    d[i - 1][j] + 1,
                    d[i][j - 1] + 1
                ),
                d[i - 1][j - 1] + substitutionCost
            );
        }
    }

    return d[m][n];
}

function searchGetWordsWithSimilarLength(word, threshold) {
    var words = [];

    for (var key of searchDict.keys()) {
        if (Math.abs(word.length - key.length) <= threshold)
            words.push(key);
    }

    return words;
}

function searchFindSimilarWord(keyword, editDistThreshold, lengthThreshold) {
    var result = [];
    var words = searchGetWordsWithSimilarLength(keyword, lengthThreshold);

    for (var word of words) {
        var editDist = searchComputeEditDistance(keyword, word);
        if (editDist <= editDistThreshold)
            result.push([word, editDist]);
    }

    result.sort(function(a, b) {
        return a[1] - b[1];
    });

    return result.map(x => x[0]);
}

function searchFindSimilarPhrases(phrase, editDistThreshold, lengthThreshold, numSuggestionsPerWord) {
    var success = true;
    var choices = [];
    var words = phrase.split(/\s+/g);

    for (var word of words) {
        var matches = searchFindSimilarWord(word, editDistThreshold, lengthThreshold);

        if (matches.length > 0) {
            var n = Math.min(matches.length, numSuggestionsPerWord);
            choices.push(matches.slice(0, n));
        } else {
            success = false;
        }
    }

    function cartesianConcat(s, t) {
        var res = [];
        
        for (var i = 0; i < s.length; i++) {
            for (var j = 0; j < t.length; j++) {
                res.push(s[i] + ' ' + t[j]);
            }
        }

        return res;
    }

    while (choices.length > 1) {
        var top = choices.pop();
        choices[choices.length - 1] = cartesianConcat(choices[choices.length - 1], top);
    }

    return [success, choices[0]];
}

function searchMakeURL(chapter, section, keyword) {
    return chapter + '.html?highlight=' + encodeURIComponent(keyword) + '#sec' + section;
}

var SearchResultType = {
    NOTHING      : 0,
    OK           : 1,
    DID_YOU_MEAN : 2,
    ERROR        : 3
};

var searchCacheSugOn = new Map();
var searchCacheSugOff = new Map();

function searchSearch(keyphrase, allowSuggestions) {
    keyphrase = searchConvertString(keyphrase);

    if (keyphrase == '') {
        return [SearchResultType.ERROR, 'Type something in order to search. Note that a lot of symbols are ignored, so the system has seen your query as empty.'];
    }

    var cached;
    if (allowSuggestions) 
        cached = searchCacheSugOn.get(keyphrase);
    else
        cached = searchCacheSugOff.get(keyphrase);

    if (cached != undefined)
        return cached;

    function countOccurencesOfPhrase(text, phrase) {
        var result = 0;
        var index = 0;

        while (true) {
            var match = text.indexOf(phrase, index);

            if (match >= 0) {
                var isSubstring = false;

                if (match > 0 && text.charAt(match - 1) != ' ')
                    isSubstring = true;

                if (match + phrase.length <= text.length - 1 && text.charAt(match + phrase.length) != ' ')
                    isSubstring = true;

                if (!isSubstring)
                    result++;

                index = match + phrase.length;
            } else {
                break;
            }
        }

        return result;
    }

    var matches = [];

    for (var i = 0; i < searchFilenames.length; i++) {
        var filename = searchFilenames[i];

        for (var section of searchFilesTransformed[filename]) {
            var isMatch = false;
            var [headline, content] = section;
            var occ = countOccurencesOfPhrase(searchConvertString(headline), keyphrase);

            if (section.length > 1)
                occ += countOccurencesOfPhrase(content, keyphrase);

            if (occ > 0) {
                var sectionName = headline.match(/^(.*?) /)[1];
                matches.push([filename, sectionName, headline, occ]);
            }
        }
    }

    if (matches.length > 0) {
        var result = [SearchResultType.OK, matches];

        if (allowSuggestions)
            searchCacheSugOn.set(keyphrase, result);
        else
            searchCacheSugOff.set(keyphrase, result);

        return result;
    }

    // No results, try to find suggestions for alternative search phrases
    if (allowSuggestions) {
        var searchSuggestionMaxSpaces = 5;

        if (keyphrase.split(' ').length > searchSuggestionMaxSpaces) {
            return [SearchResultType.ERROR, 'No results found, and the search suggestion system stopped due to an error: Too many spaces in query, maximum allowed is ' + searchSuggestionMaxSpaces + ', otherwise suggestion algorithm may be too slow and freeze the page.'];
        }

        var editDistThreshold = 5;
        var lengthThreshold = 4;
        var numSuggestionsPerWord = 3;
        var [success, choices] = searchFindSimilarPhrases(keyphrase, editDistThreshold, lengthThreshold, numSuggestionsPerWord);
        var suggestions = new Set();

        if (success) {
            for (var choice of choices) {
                var [resultType, theMatches] = searchSearch(choice, false);
                if (resultType == SearchResultType.OK)
                    suggestions.add(choice);
            }
        }
        
        // try to remove spaces if the keyphrase contains spaces
        // to try to connect words, since many danish words consist of mutiple words without spaces
        // for example a danish user might search for "spektral sætningen" when they actually want to be
        // searching for "spektralsætningen"
        var words = keyphrase.split(' ');
        if (words.length > 1) {
            for (var i = 0; i < words.length - 1; i++) {
                var phrase = '';

                for (var j = 0; j < words.length; j++) {
                    phrase += words[j];

                    if (i != j && j < words.length - 1)
                        phrase += ' ';
                }

                var [resultType, guesses] = searchSearch(phrase, true);

                if (resultType == SearchResultType.OK) {
                    suggestions.add(phrase);
                } else if (resultType == SearchResultType.DID_YOU_MEAN) {
                    for (var guess of guesses) {
                        suggestions.add(guess);
                    }
                }
            }
        }

        // Consider the following scenario: A user types "singulærværdidekomposition", but the
        // only phrase used in the book is "singulær værdi dekomposition". Assuming the individual
        // words of "singulærværdidekomposition" are spelled correctly, the following code
        // tries to guess that the user meant "singulær værdi dekomposition".
        var words = [];
        var l = 0;
        while (l < keyphrase.length) {
            var longest = null;
            var r = l + 1;
            while (r <= keyphrase.length) {
                var word = keyphrase.substring(l, r);
                if (searchDict.has(word)) {
                    longest = word;
                }
                r++;
            }

            if (longest == null)
                break;
            else {
                l += longest.length;
                words.push(longest);
            }
        }

        if (l + 1 == r) {
            // successfully added spaces to form a phrase
            var phrase = words.join(' ');
            var [resultType, _] = searchSearch(phrase, false);

            if (resultType == SearchResultType.OK)
                suggestions.add(phrase);
        }

        // TODO: Implement the above word splitting in such a way that allows for spelling mistakes (hopefully in an efficient way)

        if (suggestions.size > 0) {
            var result = [SearchResultType.DID_YOU_MEAN, Array.from(suggestions)];
            searchCacheSugOn.set(keyphrase, result);
            return result;
        }
    }

    var result = [SearchResultType.NOTHING, null];
    
    if (allowSuggestions)
        searchCacheSugOn.set(keyphrase, result);
    else
        searchCacheSugOff.set(keyphrase, result);

    return result;
}

function searchPrepareData(finishedCallback, progressCallback) {
    if (!searchShouldScrapeForData()) {
        searchSetInternalStateFromLocalStorage();
        finishedCallback();
        return;
    }

    if (searchHasBeenInit) {
        finishedCallback();
        return;
    }

    searchLoadFiles(
        function() {
            progressCallback(0);

            var fileIndex = 0;

            function step() {
                var filename = searchFilenames[fileIndex];

                searchFilesTransformed[filename] = searchTransformFile(searchFilesRaw[filename]);
                fileIndex++;

                progressCallback(fileIndex / searchFilenames.length);

                if (fileIndex < searchFilenames.length) {
                    setTimeout(step, 50);
                } else {
                    searchHasBeenInit = true;
                    finishedCallback();
                }
            }

            step();
        }
    );
}

var searchDomOverlay;
var searchDomContainer;

function searchShowInterface() {
    document.body.style.overflowY = 'hidden';

    searchDomOverlay = document.createElement('div');
    searchDomOverlay.style.backgroundColor = '#000';
    searchDomOverlay.style.opacity         = 0.7;
    searchDomOverlay.style.zIndex          = 99998;
    searchDomOverlay.style.position        = 'fixed';
    searchDomOverlay.style.left            = '0px';
    searchDomOverlay.style.top             = '0px';
    searchDomOverlay.style.width           = '100%';
    searchDomOverlay.style.height          = '100%';

    document.body.appendChild(searchDomOverlay);

    searchDomContainer = document.createElement('div');
    searchDomContainer.style.backgroundColor = '#fff';
    searchDomContainer.style.zIndex          = 99999;
    searchDomContainer.style.position        = 'fixed';
    searchDomContainer.style.left            = '15%';
    searchDomContainer.style.top             = '10%';
    searchDomContainer.style.width           = '70%';
    searchDomContainer.style.height          = '80%';
    searchDomContainer.style.padding         = '5%';
    searchDomContainer.style.paddingTop      = '0%';
    searchDomContainer.style.overflowY       = 'scroll';

    searchDomContainer.innerHTML = `
        <h1>Search</h1>
        <input id="searchInputText" type="text" placeholder="Type something and then click Find!" style="width: 75%;">
        <input id="searchFindButton" type="button" value="Find" style="width: 20%;">
        <hr>
        <div id="searchDomContainerContent">
            <p>Reading files...</p>
        </div>
    `;

    document.body.appendChild(searchDomContainer);

    var closeButton = document.createElement('input');

    closeButton.type           = 'button';
    closeButton.value          = '\xA0\xD7\xA0';
    closeButton.style.position = 'absolute';
    closeButton.style.right    = '5%';
    closeButton.style.top      = '5%';

    closeButton.addEventListener('click', function() {
        searchHideInterface();
    })

    searchDomContainer.appendChild(closeButton);

    searchPrepareData(function() {
        var content = document.getElementById('searchDomContainerContent');

        content.innerHTML = `
            <p></p>
        `;

        if (searchShouldScrapeForData()) {
            var data = searchGetInternalStateJSON();
            window.localStorage.setItem(searchLocalStorageKey, data);
        }
    }, function(progress) {
        var content = document.getElementById('searchDomContainerContent');

        content.innerHTML = `
            <p>Please wait. Preparing data... (${(100 * progress).toFixed(1)}%)</p>
        `;
    });

    var findButton = document.getElementById('searchFindButton');

    searchInputText.addEventListener('keydown', function(event) {
        if (event.key == 'Enter') {
            document.getElementById('searchFindButton').click();
        }
    });

    findButton.addEventListener('click', function() {
        if (!searchHasBeenInit) {
            window.alert("Search is not ready!");
            return;
        }

        var query = document.getElementById('searchInputText').value;
        var content = document.getElementById('searchDomContainerContent');
        var [resultType, matches] = searchSearch(query, true);

        if (resultType == SearchResultType.OK) {
            var list = [];

            for (var i = 0; i < matches.length; i++) {
                var [chapter, sectionName, sectionDisplayName, numMatches] = matches[i];
                list.push(`
                    <li>
                        <p>
                            <a href="${searchMakeURL(chapter, sectionName, searchConvertString(query))}" target="_blank">${sectionDisplayName}</a>
                            <span style="color: #ccc;">(${numMatches} match${numMatches != 1 ? 'es' : ''})</span>
                        </p>
                    </li>
                `);
            }

            content.innerHTML = `
                <h2>Matches for &#8220;${query}&#8221;:</h2>
                <ul>
                    ${list.join('\n')}
                </ul>
            `;
        } else if (resultType == SearchResultType.DID_YOU_MEAN) {
            var list = [];
            
            for (var i = 0; i < matches.length; i++) {
                var match = matches[i];
                list.push(`<li><p><a href="#" id="searchDYM_${i}">${match}</a>?</p></li>`);
            }

            content.innerHTML = `
                <h2>Did you mean:</h2>
                <ul>
                    ${list.join('\n')}
                </ul>
            `;

            function makeClickListener(suggestion) {
                return function(event) {
                    event.preventDefault();
                    document.getElementById('searchInputText').value = suggestion;
                    findButton.click();
                };
            }

            for (var i = 0; i < matches.length; i++) {
                var match = matches[i];
                document.getElementById(`searchDYM_${i}`).addEventListener('click', makeClickListener(match));
            }
        } else if (resultType == SearchResultType.NOTHING) {
            content.innerHTML = `
                <p>Nothing matched your search "${query}"</p>
            `;
        } else if (resultType == SearchResultType.ERROR) {
            content.innerHTML = `
                <h2>Error:</h2>
                <ul>
                    <p>${matches}</p>
                </ul>
            `;
        }
    });
}

function searchHideInterface() {
    document.body.removeChild(searchDomContainer);
    document.body.removeChild(searchDomOverlay);
    document.body.style.overflowY = 'auto';
}

function searchHighlightPhraseOnSite(phrase) {
    /*var regExp = new RegExp(`\\b${phrase}\\b`, 'gi');

    function rec(node) {
        var child = node.firstChild;

        while (child) {
            switch (child.nodeType) {
                case Node.TEXT_NODE:
                    var original = child.textContent;
                    var newText = original;

                    newText = newText.replace(regExp, function(x) {
                        return `@@@${x}@@@`;
                    });
                    
                    if (newText != original) {
                        child.replaceData(0, original.length, newText);
                    }

                    break;

                case Node.ELEMENT_NODE:
                    if (!child.classList.contains('btn'))
                        rec(child);
                    
                    break;
            }

            child = child.nextSibling;
        }
    }

    rec(document.body.querySelector('.main'));

    var mainHTML = String(document.querySelector('.main').innerHTML);
    
    mainHTML = mainHTML.replace(
        /@@@(.*?)@@@/g,
        function(_, inner) {
            return `<span class="searchHighlight">${inner}</span>`;
        }
    );
    
    document.querySelector('.main').innerHTML = mainHTML;*/

    // went with a quite nice library here since the above code made the quizzes stop working

    var options = {
        "element": "span",
        "className": "searchHighlight",
        "separateWordSearch": false,
        "accuracy": {
            "value": "exactly",
            "limiters": ":;.,-_()!?'\"".split("")
        },
        "ignorePunctuation": ":;.,-_()!?'\"".split("")
    };

    var context = document.querySelector('.main');
    var instance = new Mark(context);
    instance.mark(phrase, options);
}

function searchDomReady() {
    // set the document title to be the name of the chapter
    try {
        document.title = document.querySelector('h1 span').innerText;
    } catch (e) {}

    // populate searchFilenames array
    // this is a hacky solution where all the html files are found in the table
    // of contents in the sidenav, ideally this variable should just be set from
    // within the Python code.
    var sidebar = String(document.querySelector('.sidenav').innerHTML);
    var pages = new Set();
    var matches = sidebar.match(/href=(.*?)\.html/g);    
    for (var item of matches) {
        var match = item.match(/([\w\d]+)\.html/);
        pages.add(match[1]);
    }

    searchFilenames = Array.from(pages);

    // create styles
    var style = document.createElement('style');

    style.innerHTML = `
        .searchHighlight {
            margin: 3px;
            padding: 3px;
            background-color: #ff9;
            border: thin solid #f5bc42;
        }

        .searchIcon {
            z-index: 99997;
            cursor: pointer;
            position: fixed;
            left: 15px;
            bottom: 15px;
            padding: 0;
            margin: 0;
            width: 30px;
            height: 30px;
            animation-duration: 0.3s;
            animation-iteration-count: 1;
            transform-origin: bottom;
        }

        .searchIcon:hover {
            animation-name: bounce;
            animation-timing-function: ease;
        }

        @keyframes bounce {
            0%   { transform: translateY(0); }
            50%  { transform: translateY(-5px); }
            100% { transform: translateY(0); }
        }
    `;

    document.head.appendChild(style);

    var icon = document.createElement('div');
    
    icon.classList.add('searchIcon');
    icon.innerHTML = `
        <img src="img/Magnifying_glass_icon.svg" style="padding: 0; margin: 0; width: 100%; height: 100%;">
    `; // This magnifying glass icon is in public domain, see https://commons.wikimedia.org/wiki/File:Magnifying_glass_icon.svg

    icon.addEventListener('click', function() {
        searchShowInterface();
    });

    document.body.appendChild(icon);

    var urlParams = new URLSearchParams(document.location.search);
    if (urlParams.has('highlight'))
        searchHighlightPhraseOnSite(urlParams.get('highlight'));
}

if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', searchDomReady);
} else {
    searchDomReady();
}