document.addEventListener('DOMContentLoaded', function () {
    console.log("testing console log");

    // Retrieve the API URL from chrome.storage.local
    chrome.storage.local.get(['apiURL'], function (result) {
        if (chrome.runtime.lastError) {
            console.error('Error retrieving API URL:', chrome.runtime.lastError);
        } else {
            const apiUrl = result.apiURL;
            console.log('Retrieved API URL:', apiUrl);
            // Store the API URL in chrome.storage.local
            chrome.storage.local.set({ 'apiUrl': apiUrl }, function () {
                if (chrome.runtime.lastError) {
                    console.error('Error setting API URL:', chrome.runtime.lastError);
                }
            });
        }
    });

    console.log("starting login test");
    // Add event listener for when user clicks submit
    const loginForm = document.querySelector('form');
    const messageDiv = document.createElement('div');
    loginForm.parentElement.appendChild(messageDiv);

    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Retrieve API URL from chrome.storage.local
        chrome.storage.local.get(['apiUrl'], async function (result) {
            const apiUrl = result.apiUrl;
            if (!apiUrl) {
                console.error('API URL not found in chrome.storage.local');
                return;
            }

            const email = loginForm.querySelector('input[type="email"]').value;
            const password = loginForm.querySelector('input[type="password"]').value;
            const loginUrl = `${apiUrl}/login`;

            try {
                const response = await fetch(loginUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: new URLSearchParams({
                        username: email,
                        password: password
                    })
                });

                console.log('Response Status:', response.status);
                console.log('Response OK:', response.ok);

                const responseText = await response.text();
                console.log('Response Text:', responseText);

                if (!response.ok) {
                    throw new Error('Invalid credentials');
                }

                // Parse the response JSON
                const data = JSON.parse(responseText);
                const accessToken = data.access_token;
                console.log('Access Token:', accessToken);

                // Store JWT in chrome.storage.local
                chrome.storage.local.set({ 'access_token': accessToken }, function () {
                    if (chrome.runtime.lastError) {
                        console.error('Error setting access token:', chrome.runtime.lastError);
                    } else {
                        messageDiv.classList.remove('d-none', 'alert-danger');
                        messageDiv.classList.add('alert', 'alert-success');
                        messageDiv.innerText = 'Login successful!';

                        setTimeout(() => {
                            window.close();
                        }, 2000);
                    }
                });

            } catch (error) {
                console.error('Error during login:', error);
                messageDiv.classList.remove('d-none', 'alert-success');
                messageDiv.classList.add('alert', 'alert-danger');
                messageDiv.innerText = error.message;
            }
        });
    });
});
