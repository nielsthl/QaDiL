// Function to check for file changes, reload the page, and handle scroll position
function checkForChangesAndReload() {
    const currentURL = window.location.href;

    $.ajax({
        type: 'HEAD',
        url: currentURL,
        success: function(data, status, xhr) {
          const currentTimestamp = new Date(xhr.getResponseHeader('Last-Modified')).getTime();

          // Check if file has changed
          if (currentTimestamp > lastModifiedTimestamp) {
            // File has changed, reload the page
            console.log('Reloading the page...');
            location.reload();
          } else {
            // Restore the scroll position
            const savedScrollPos = localStorage.getItem('scrollPos');
            if (savedScrollPos !== null) {
              $(window).scrollTop(parseInt(savedScrollPos));
            }
          }

          // Update the timestamp and store it in localStorage
          lastModifiedTimestamp = currentTimestamp;
          localStorage.setItem('lastModifiedTimestamp', lastModifiedTimestamp);
        }
    });
}

// Open all buttons
$(".envbuttons").collapse('show');

// When the user scrolls, save the scroll position
$(window).on('scroll', function() {
    localStorage.setItem('scrollPos', $(window).scrollTop());
});

// When the page is loaded
$(document).ready(function() {
    // Initialize lastModifiedTimestamp from localStorage, if available
    lastModifiedTimestamp = localStorage.getItem('lastModifiedTimestamp');
    if (lastModifiedTimestamp === null) {
	lastModifiedTimestamp = 0;
    } else
	lastModifiedTimestamp = parseInt(lastModifiedTimestamp);
 
      checkForChangesAndReload(); // Check for file changes and handle scroll position (initial check)

      // Check for changes and handle scroll position every 2 seconds (adjust as needed)
      setInterval(checkForChangesAndReload, 2000);
});
