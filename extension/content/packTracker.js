/**
 * 
 * 
 */

// Retrieve the API URL from chrome.storage.local
chrome.storage.local.get(['apiURL'], function(result) {
    if (chrome.runtime.lastError) {
        console.error('Error retrieving API URL:', chrome.runtime.lastError);
    } else {
        const apiUrl = result.apiURL;
        console.log('Retrieved API URL:', apiUrl);
        // Use the API URL as needed
        localStorage.setItem('apiUrl', apiUrl)
    }
});



// Create a MutationObserver to watch for changes in the DOM
const observerCallback = (mutationsList, observer) => {
    // Call both functions to handle packs and picks
    addEventListenersToPacks();
    addEventListenersToPicks();
};

// Create a MutationObserver instance
const observer = new MutationObserver(observerCallback);

// Start observing the document body for changes
observer.observe(document.body, {
    childList: true,
    subtree: true
});