document.addEventListener('DOMContentLoaded', function() {
    // Retrieve both the access_token and apiURL from chrome.storage.local
    chrome.storage.local.get(['access_token', 'apiURL'], function(items) {
        const access_token = items.access_token;
        const apiURL = items.apiURL;

        // Check if apiURL is available
        if (!apiURL) {
            console.error('API URL is not set.');
            // Handle the case where apiURL is not set
            document.body.innerHTML = `<object type="text/html" data="login.html" width="100%" height="100%"></object>`;
            return;
        }
        console.log("access_token: ", access_token)
        // Check if token exists
        if (!access_token) {
            // No token found, show login page
            document.body.innerHTML = `<object type="text/html" data="login.html" width="100%" height="100%"></object>`;
            return;
        }

        // Token exists, verify it
        fetch(`${apiURL}/login/verify-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                access_token: access_token,
                token_type: 'bearer' // Adjust if your token_type is different
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_valid) {
                console.log("this is valid data : ", data)
                // Token is valid, show logout page
                document.body.innerHTML = `<object type="text/html" data="logout.html" width="100%" height="100%"></object>`;
            } else {
                console.log("this is the invalid data : ", data)

                // Token is not valid, show login page
                document.body.innerHTML = `<object type="text/html" data="login.html" width="100%" height="100%"></object>`;
            }
        })
        .catch(error => {
            console.error('Error verifying token:', error);
            // In case of an error, show login page
            document.body.innerHTML = `<object type="text/html" data="login.html" width="100%" height="100%"></object>`;
        });
    });
});
