chrome.runtime.onInstalled.addListener(() => {
    console.log('EAFC Pack Tracker extension installed');
});

// Define the API URL based on the extension's installation type
chrome.management.get(chrome.runtime.id, function(extensionInfo) {
    let apiUrl;

    if (extensionInfo.installType === 'development') {
        apiUrl = 'http://localhost:8000';
    } else {
        apiUrl = 'Temp url';
    }

    // Store the API URL in chrome.storage.local
    chrome.storage.local.set({ "apiURL": apiUrl }, function() {
        if (chrome.runtime.lastError) {
            console.error('Error setting API URL:', chrome.runtime.lastError);
        } else {
            console.log('API URL is set: ', apiUrl);
        }
    });
});

