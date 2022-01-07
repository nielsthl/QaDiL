var bubbleLabels;
var bubbleContents;
var bubbleCaptures;
var bubbleActive;
var bubbleCheckerIsRunning = false;

function placeBubble(bubbleLabel, bubbleContent) {
    bubbleContent.style.left = Math.round(bubbleLabel.offsetLeft + bubbleLabel.offsetWidth / 2 - bubbleContent.offsetWidth / 2) + 'px';
    bubbleContent.style.top  = Math.round(bubbleLabel.offsetTop - bubbleContent.offsetHeight - 6) + 'px';
}

function placeBubbles() {
    for (var i = 0; i < bubbleLabels.length; i++) {
        var bubbleLabel = bubbleLabels[i];
        var bubbleContent = bubbleContents[i];

        placeBubble(bubbleLabel, bubbleContent);
    }
}

function makeBubbleLabelMouseOver(index, label, content) {
    return function() {
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
    bubbleLabels = document.querySelectorAll('.bubblelabel');
    bubbleContents = document.querySelectorAll('.bubblecontent');
    bubbleCaptures = new Array(bubbleLabels.length).fill(0);
    bubbleActive = [];

    placeBubbles();

    for (var i = 0; i < bubbleLabels.length; i++) {
        var bubbleLabel = bubbleLabels[i];
        var bubbleContent = bubbleContents[i];

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