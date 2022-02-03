var bubbleMouseX = 0, bubbleMouseY = 0;
var bubbleLabels;
var bubbleContents;
var bubbleCaptures;
var bubbleActive;
var bubbleCheckerIsRunning = false;
var bubbleBoundingBox = null;

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

function boundingBoxContainedInBoundingBox(candidate, box) {
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
}

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
    var offsets = [
        // regular OK
        [- bubbleContent.offsetWidth / 2, - bubbleContent.offsetHeight - 6, []],

        // left OK
        [- bubbleContent.offsetWidth * 0.08, - bubbleContent.offsetHeight - 6, ['bubbleleft']],

        // left flipped OK
        [- bubbleContent.offsetWidth * 0.08, 38, ['bubbleleft', 'bubbleflipped']],

        // right OK
        [- bubbleContent.offsetWidth * 0.92, - bubbleContent.offsetHeight - 6, ['bubbleright']],

        // right flipped
        [- bubbleContent.offsetWidth * 0.92, 38, ['bubbleright', 'bubbleflipped']]
    ];

    var start = 0;
    for (var i = start; i < offsets.length; i++) {
        var [offsetX, offsetY, classes] = offsets[i];

        for (var className of allClasses) {
            if (classes.indexOf(className) >= 0) {
                bubbleContent.classList.add(className);
            } else {
                bubbleContent.classList.remove(className);
            }
        }

        bubbleContent.style.left = Math.round(targetX + offsetX) + 'px';
        bubbleContent.style.top  = Math.round(targetY + offsetY) + 'px';

        if (boundingBoxContainedInBoundingBox(
            [bubbleContent.offsetLeft, bubbleContent.offsetTop, bubbleContent.offsetWidth, bubbleContent.offsetHeight],
            [window.scrollX, window.scrollY, window.innerWidth, window.innerHeight]
        )) {
            break;
        }
    }

    /*
    bubbleBoundingBox.style.left = bubbleContent.offsetLeft + 'px';
    bubbleBoundingBox.style.top = bubbleContent.offsetTop + 'px';
    bubbleBoundingBox.style.width = bubbleContent.offsetWidth + 'px';
    bubbleBoundingBox.style.height = bubbleContent.offsetHeight + 'px';
    */

    /*
    bubbleBoundingBox.style.left = (window.scrollX + 5) + 'px';
    bubbleBoundingBox.style.top = (window.scrollY + 5) + 'px';
    bubbleBoundingBox.style.width = (window.innerWidth - 10) + 'px';
    bubbleBoundingBox.style.height = (window.innerHeight - 10) + 'px';
    */
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
    bubbleBoundingBox = document.createElement('div');
    bubbleBoundingBox.style.margin   = 0;
    bubbleBoundingBox.style.padding  = 0;
    bubbleBoundingBox.style.zIndex   = -1;
    bubbleBoundingBox.style.position = 'absolute';
    bubbleBoundingBox.style.left     = '5px';
    bubbleBoundingBox.style.top      = '5px';
    bubbleBoundingBox.style.width    = '50px';
    bubbleBoundingBox.style.height   = '50px';
    bubbleBoundingBox.style.border   = 'thin solid #f00';

    document.body.appendChild(bubbleBoundingBox);

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

if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', initBubbles);
} else {
    initBubbles();
}