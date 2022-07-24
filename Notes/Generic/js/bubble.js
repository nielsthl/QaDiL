var bubbleMouseX = 0, bubbleMouseY = 0;
var bubbleLabels;
var bubbleContents;
var bubbleCaptures;
var bubbleActive;
var bubbleCheckerIsRunning = false;

function distToBoundingBox(left, top, width, height, x, y) {
    /*      .                   .
            . #2                .
        ....@___________________ ....
            |\                  |
        #1  | (left, top)       | #3
            |                   |
            |                   |
            |                   |
        ....|___________________|....
            .                   .
            . #4                .
    */

    var xDist = 0;
    var yDist = 0;

    if (x < left)         xDist = left - x;           // #1
    if (y < top)          yDist = top - y;            // #2
    if (x > left + width) xDist = x - (left + width); // #3
    if (y > top + height) yDist = y - (top + height); // #4

    return Math.sqrt(xDist * xDist + yDist * yDist);
}

function boundingBoxIntersectionArea(box1, box2) {
    function intersect1D(a, b, c, d) {
        if (b < c || d < a)
            return 0;

        return Math.min(b, d) - Math.max(a, c);
    }
    
    var [x1, y1, w1, h1] = box1;
    var [x2, y2, w2, h2] = box2;
    
    return intersect1D(x1, x1 + w1, x2, x2 + w2) * intersect1D(y1, y1 + h1, y2, y2 + h2);
}

/*function boundingBoxContainedInBoundingBox(candidate, box) {
    var [candidateLeft, candidateTop, candidateWidth, candidateHeight] = candidate;
    var [left, top, width, height] = box;
    var eps = 1e-6;
    
    if (distToBoundingBox(left, top, width, height, candidateLeft, candidateTop) >= eps)
        return false;
    
    if (distToBoundingBox(left, top, width, height, candidateLeft + candidateWidth, candidateTop) >= eps)
        return false;

    if (distToBoundingBox(left, top, width, height, candidateLeft, candidateTop + candidateHeight) >= eps)
        return false;
    
    if (distToBoundingBox(left, top, width, height, candidateLeft + candidateWidth, candidateTop + candidateHeight) >= eps)
        return false;

    return true;
}*/

function placeBubble(bubbleLabel, bubbleContent) {
    var spans = bubbleLabel.querySelectorAll('span');
    var allWordsOnSameLine = true;
    var prev;
    
    for (var i = 0; i < spans.length; i++) {
        var span = spans[i];

        if (i > 0 && span.offsetTop != prev) {
            allWordsOnSameLine = false;
            break;
        }

        prev = span.offsetTop;
    }

    var targetX, targetY;

    if (allWordsOnSameLine) {
        targetX = Math.round(bubbleLabel.offsetLeft + bubbleLabel.offsetWidth / 2);
        targetY = Math.round(bubbleLabel.offsetTop);
    } else {
        var closestIndex = -1;
        var closestDist = Number.POSITIVE_INFINITY;
        
        for (var i = 0; i < spans.length; i++) {
            var span = spans[i];
            var dist = distToBoundingBox(span.offsetLeft, span.offsetTop, span.offsetWidth, span.offsetHeight, bubbleMouseX, bubbleMouseY);

            if (dist <= closestDist) {
                closestIndex = i;
                closestDist = dist;
            }
        }

        var chosenSpan = spans[closestIndex];

        targetX = Math.round(chosenSpan.offsetLeft + chosenSpan.offsetWidth / 2);
        targetY = Math.round(chosenSpan.offsetTop);
    }

    var allClasses = ['bubbleleft', 'bubbleright', 'bubbleflipped'];
    var layouts = [
        [- bubbleContent.offsetWidth * 0.50, - bubbleContent.offsetHeight - 6, []],
        [- bubbleContent.offsetWidth * 0.50, 38,                               ['bubbleflipped']],
        [- bubbleContent.offsetWidth * 0.95, - bubbleContent.offsetHeight - 6, ['bubbleright']],
        [- bubbleContent.offsetWidth * 0.95, 38,                               ['bubbleright', 'bubbleflipped']],
        [- bubbleContent.offsetWidth * 0.05, - bubbleContent.offsetHeight - 6, ['bubbleleft']],
        [- bubbleContent.offsetWidth * 0.05, 38,                               ['bubbleleft', 'bubbleflipped']]
    ];

    function setLayout(index) {
        var [offsetX, offsetY, classes] = layouts[index];

        for (var className of allClasses) {
            if (classes.indexOf(className) >= 0) {
                bubbleContent.classList.add(className);
            } else {
                bubbleContent.classList.remove(className);
            }
        }

        bubbleContent.style.left = Math.round(targetX + offsetX) + 'px';
        bubbleContent.style.top  = Math.round(targetY + offsetY) + 'px';
    }

    var areaPairs = [];

    for (var i = 0; i < layouts.length; i++) {
        setLayout(i);

        var computedArea = boundingBoxIntersectionArea(
            [bubbleContent.offsetLeft, bubbleContent.offsetTop, bubbleContent.offsetWidth, bubbleContent.offsetHeight],
            [window.scrollX, window.scrollY, window.innerWidth, window.innerHeight]
        );

        areaPairs.push({index: i, area: computedArea});
    }

    areaPairs.sort(function(lhs, rhs) {
        if (rhs.area - lhs.area != 0)
            return rhs.area - lhs.area;

        return lhs.index - rhs.index;
    });

    setLayout(areaPairs[0].index);
}

function placeBubbles() {
    for (var i = 0; i < bubbleLabels.length; i++) {
        var bubbleLabel = bubbleLabels[i];
        var bubbleContent = bubbleContents[i];

        placeBubble(bubbleLabel, bubbleContent);
    }
}

function makeBubbleLabelMouseOver(index, label, content) {
    return function(event) {
        bubbleMouseX = event.pageX;
        bubbleMouseY = event.pageY;
        placeBubble(label, content);
        content.classList.add('bubblestick');
        bubbleCaptures[index]++;
        bubbleActive.push(index);
        startBubbleChecker();
    }
}

function makeBubbleLabelMouseOut(index, label, content) {
    return function() {
        bubbleCaptures[index]--;
    }
}

function makeBubbleContentMouseOver(index, label, content) {
    return function() {
        bubbleCaptures[index]++;
    }
}

function makeBubbleContentMouseOut(index, label, content) {
    return function() {
        bubbleCaptures[index]--;
    }
}

function initBubbles() {
    setupRefBubbles();

    bubbleLabels = document.querySelectorAll('.bubblelabel');
    bubbleContents = document.querySelectorAll('.bubblecontent');
    bubbleCaptures = new Array(bubbleLabels.length).fill(0);
    bubbleActive = [];

    placeBubbles();

    for (var i = 0; i < bubbleLabels.length; i++) {
        var bubbleLabel = bubbleLabels[i];
        var bubbleContent = bubbleContents[i];
        var words = bubbleLabel.innerText.split(' ');
        
        bubbleLabel.innerHTML = words.map(x => `<span>${x}</span>`).join(' ');
        bubbleLabel.addEventListener('mouseover', makeBubbleLabelMouseOver(i, bubbleLabel, bubbleContent));
        bubbleLabel.addEventListener('mouseout', makeBubbleLabelMouseOut(i, bubbleLabel, bubbleContent));
        bubbleContent.addEventListener('mouseover', makeBubbleContentMouseOver(i, bubbleLabel, bubbleContent));
        bubbleContent.addEventListener('mouseout', makeBubbleContentMouseOut(i, bubbleLabel, bubbleContent));
    }

    window.addEventListener('resize', placeBubbles);
}

function startBubbleChecker() {
    if (!bubbleCheckerIsRunning) {
        bubbleCheckerIsRunning = true;
        bubbleChecker();
    }
}

function bubbleChecker() {
    var keepRunning = false;

    for (var i = 0; i < bubbleActive.length; i++) {
        var index = bubbleActive[i];
        if (bubbleCaptures[index] == 0) {
            bubbleContents[index].classList.remove('bubblestick');
        } else {
            keepRunning = true;
        }
    }

    if (keepRunning) {
        setTimeout(bubbleChecker, 250);
    } else {
        bubbleActive = [];
        bubbleCheckerIsRunning = false;
    }
}

function refBubbleGetFilename(url) {
    return url.match(/\/(\w+)\.html/)[1];
}

function refBubbleGetEquId(url) {
    return url.match(/#equ([a-zA-Z0-9\.]+)/)[1];
}

function refBubbleGetEnvId(url) {
    return url.match(/#env([a-zA-Z0-9\.]+)/)[1];
}

function refBubbleGetHashtag(url) {
    return url.split('#')[1];
}

var refBubbleLocalStorageKey = 'QaDiLRefData';
var refBubbleData = new Map();
var refBubblePagesToFetch = new Map();

function refBubbleEnvKey(page, envId) {
    return `${page}-env${envId}`;
}

function refBubbleEquKey(page, envId) {
    return `${page}-equ${envId}`;
}

function refBubbleFetchPage(page) {
    if (!refBubblePagesToFetch.has(page))
        refBubblePagesToFetch.set(page, []);

    return refBubblePagesToFetch.get(page);
}

function refBubbleFetchExternalEnv(page, envId) {
    var key = refBubbleEnvKey(page, envId);

    if (refBubbleData.has(key))
        return refBubbleData.get(key);
    
    var list = refBubbleFetchPage(page);
    list.push('env' + envId);

    return 'Loading...';
}

function refBubbleExtractHTMLBody(data) {
    var start = data.indexOf('<body>');
    var end = data.indexOf('</body>', start);

    return data.substring(start + '<body>'.length, end);
}

function refBubbleRenderTeX() {
    // This code is taken from the header, which sets up KaTeX stuff
    // -- we need to run it again on the TeX extracted from the other pages
    var tex = document.querySelectorAll('script[type^="math/tex"]');

    for(var i = 0; i < tex.length; ++i) {
        var display = tex[i].getAttribute('type').indexOf('mode=display') > -1;
        
        var math = tex[i].previousSibling;
        math.className = 'katex-render';
        
        var content = tex[i].textContent;
        
        katex.render(content, math, {
            /* output: html, */
            displayMode: display,
            throwOnError: false,
            trust: true
        });
        
        tex[i].parentNode.removeChild(tex[i]);
    }
}

function refBubbleFetchPages() {
    var pagesLoaded = 0;
    var pagesTotal = 0;

    function makeHandler(fileName) {
        return function() {
            var fragment = document.createDocumentFragment();
            var div = document.createElement('div');

            div.innerHTML = refBubbleExtractHTMLBody(this.responseText);
            fragment.appendChild(div);

            var lookup = refBubblePagesToFetch.get(fileName);

            for (var key of lookup) {
                var number = key.replace('env', '');
                var html = refBubbleGetEnvBubbleHTML(fragment, number);
                var index = 0;

                while (true) {
                    var htmlKey = 'refbubble-env' + number + '-inst' + index;
                    var element = document.getElementById(htmlKey);

                    if (!element)
                        break;

                    element.innerHTML = html;
                    index++;
                }
            }

            pagesLoaded++;

            if (pagesLoaded == pagesTotal)
                refBubbleRenderTeX();
        };
    }
    
    for (var key of refBubblePagesToFetch.keys()) {
        pagesTotal++;

        var request = new XMLHttpRequest();
        
        request.addEventListener('load', makeHandler(key));
        request.open('GET', key + '.html', true);
        request.send();
    }
}

function refBubbleGetEnvBubbleHTML(model, envId) {
    var elementToCopy = model.querySelector(`*[data-count="${envId}"]`);
    var className;
    var elementContent;

    try {
        className = elementToCopy.classList.item(0);

        if (className == 'Exerciseno') {
            var buttonElement = model.querySelector(`*[data-count="${envId}"] + a`);
            var divId = refBubbleGetHashtag(buttonElement.href);
            
            elementContent = model.getElementById(divId).innerHTML;
        } else {
            elementContent = elementToCopy.innerHTML;
        }

        elementContent = elementContent.replace(/id="(.*?)"/g, function(_, ID) {
            return `id="copy-${ID}"`;
        });

        elementContent = elementContent.replace(/href="#(.*?)"/g, function(_, ID) {
            return `href="#copy-${ID}"`;
        });
    } catch (err) {
        elementContent = 'An error occured: ' + err.message;
    }
    
    return '<div class="' + className + '" data-count="' + envId + '">' + elementContent + '</div>';
}

function setupRefBubbles() {
    var currentPage = refBubbleGetFilename(document.location.href);
    var links = document.querySelectorAll('a');
    var instanceCounter = new Map();

    for (var i = 0; i < links.length; i++) {
        var link = links[i];

        if (link.href.indexOf('#env') >= 0) {
            var fileName = refBubbleGetFilename(link.href);
            var envId = refBubbleGetEnvId(link.href);
            var content = document.createElement('div');

            if (!instanceCounter.has(envId)) {
                instanceCounter.set(envId, 0);
            } else {
                instanceCounter.set(envId, instanceCounter.get(envId) + 1);
            }

            content.id = 'refbubble-env' + envId + '-inst' + instanceCounter.get(envId);
            
            link.classList.add('bubblelabel');
            content.classList.add('bubblecontent');

            if (fileName == currentPage) {
                content.innerHTML = refBubbleGetEnvBubbleHTML(document, envId);
            } else {
                content.innerHTML = refBubbleFetchExternalEnv(fileName, envId);
            }

            link.parentNode.insertBefore(content, link.nextSibling);
        } else if (link.href.indexOf('#equ') >= 0) {
            var equId = refBubbleGetEquId(link.href);
            var content = document.createElement('div');
            
            link.classList.add('bubblelabel');
            content.classList.add('bubblecontent');

            if (refBubbleGetFilename(link.href) == currentPage) {
                var elementToCopy = document.querySelector(`*[id="equ${equId}"] + div`);

                content.innerHTML = elementToCopy.innerHTML;
            } else {
                content.innerHTML = 'Equation from external page'; // TODO
            }

            link.parentNode.insertBefore(content, link.nextSibling);
        }
    }

    var tags = document.querySelectorAll('.bubblecontent .tag');

    for (var i = 0; i < tags.length; i++) {
        var tag = tags[i];
        tag.style.display = 'none';
    }

    refBubbleFetchPages();
}

if (document.readyState != 'complete') {
    window.addEventListener('load', initBubbles);
} else {
    initBubbles();
}