/**
 * addEventListenersToPicks will be triggered when ever a change in the DOM is detected
 * It will look for the presence of the Redeem Player Pick button
 * If picks are located on screen event listeners will be added to the Redeem button for each pick
 * Upon a click it will trigger the function handlePackOpened
 */
function addEventListenersToPicks() {
    // Select all buttons and find the one with the text: 'Redeem Player Picks Item'
    const redeemButton = Array.from(document.querySelectorAll('button'))
        .find(button => button.querySelector('.btn-text')?.textContent.trim() === 'Redeem Player Picks Item');

    if (redeemButton) {
        // Find the closest parent element that contains the pick name
        const detailPanel = redeemButton.closest('.DetailPanel');
        const pickNameElement = detailPanel?.querySelector('.subHeading');
        const pickName = pickNameElement ? pickNameElement.textContent.trim() : 'Unknown Pick';

        if (!redeemButton.dataset.listenerAdded) {
            redeemButton.dataset.listenerAdded = 'true'; // Mark as having the listener added

            console.log(`Added an event listener to pick: ${pickName}`);

            // Add click event listener to the Redeem button
            redeemButton.addEventListener('click', () => {
                // Delay the execution of handlePickOpened by 1 second to allow for DOM to load after animation
                setTimeout(() => {
                    handlePickOpened(pickName); 
                }, 1000); 
            });    
        }
    } 
}


/**
 * Store each pick in pickItems and iterate through each pick and store the data of each pick
 * addEventListenersToPickItems is used to then add an event listener to each pick element to determine
 * which element is currently selected by the user
 * @param {string} pickName - name of the player pick opened
 */
function handlePickOpened(pickName) {
    console.log(`Player Pick: ${pickName} has been opened`);
    
    const pickItems = document.querySelectorAll(".player-pick-option");
    // Array to hold all item data
    let itemsData = [];

    pickItems.forEach(item => {
        // Get the players name, rating, position, isTradeable, isDuplicate
        let itemData = extractKeyPlayerAttributes(item, 'pick');
        itemData.pack_name = pickName
        const position = itemData.position
        // Populate attributes based on player position
        if (position === "GK") {
            const diving = item.querySelector(".Pace.statValue").textContent.trim();
            const handling = item.querySelector(".Shooting.statValue").textContent.trim();
            const kicking = item.querySelector(".Passing.statValue").textContent.trim();
            const reflexes = item.querySelector(".Dribbling.statValue").textContent.trim();
            const speed = item.querySelector(".Defending.statValue").textContent.trim();
            const positioning = item.querySelector(".Header.statValue").textContent.trim();
            itemData = {
                ...itemData,
                diving,
                handling,
                kicking,
                reflexes,
                speed,
                positioning
            };
        } else {
            const shooting = item.querySelector(".Shooting.statValue").textContent.trim();
            const dribbling = item.querySelector(".Dribbling.statValue").textContent.trim();
            const passing = item.querySelector(".Passing.statValue").textContent.trim();
            const pace = item.querySelector(".Pace.statValue").textContent.trim();
            const defending = item.querySelector(".Defending.statValue").textContent.trim();
            const physical = item.querySelector(".Header.statValue").textContent.trim();
            itemData = {
                ...itemData,
                shooting,
                dribbling,
                passing,
                pace,
                defending,
                physical
            };
        }

        // Add item to itemsData array
        itemsData.push(itemData);

    })
    // Add event listener to each pick to see which one is selectedand currently active
    // When the Confirm button is clicked it will add the value: isSelected to that player
    itemsData = addEventListenersToPickItems(itemsData, pickItems, pickName)
    console.log('Item all data:', itemsData);

}

/**
 * This function is called after a user opens a player pick and is shown a selction of players to choose from
 * The is_selected field is added to itemsData to indicate the current player pick choice
 * It will add eventlistener to each pick so that when the user selects a new pick, is_selected gets updated for each value
 * It will use a mutation observer to detect when the success message is shown and send the itemsData to the backend
 * @param {Array} itemsData 
 * @param {NodeList} pickItems 
 * @param {String} packName 
 * @returns 
 */
function addEventListenersToPickItems(itemsData, pickItems, packName) {
    // The first pick is automatically selected when opened
    itemsData.forEach((item, idx) => {
        item.is_selected = (idx === 0); 
    });

    // Add event listeners to the items of the player pick to see which one is selected
    pickItems.forEach((pick, index) => {
        if (!pick.dataset.listenerAdded) {
            pick.dataset.listenerAdded = 'true';

            // Add event listener to the pick item
            pick.addEventListener('click', () => {
                // Update isSelected values
                itemsData.forEach((item, idx) => {
                    item.is_selected = (index === idx);
                });
            });
        }
    });

    // Flag to ensure that API request is sent only once
    let apiRequestSent = false;

    // Function to handle the success detection
    const detectSuccess = () => {
        if (apiRequestSent) return; // Exit if the API request has already been sent

        const rewardsCarousel = document.querySelector('.rewards-carousel');
        if (rewardsCarousel) {

            if (packName) {
                apiRequestSent = true; // Set flag to prevent further API requests
                sendBatchDataToBackend({ pack_name: packName, items: itemsData }, 'http://localhost:8000/picks');

                playerPickObserver.disconnect(); // Disconnect the observer once the success element is found
            } else {
                console.error('packName is not defined.');
            }
        }
    };

    // Create a MutationObserver instance
    const playerPickObserver = new MutationObserver((mutationsList, observer) => {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                detectSuccess();
            }
        }
    });

    // Start observing the document body for changes
    playerPickObserver.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Set a timeout to stop observing after 10 seconds if the element is not found
    setTimeout(() => {
        playerPickObserver.disconnect();
        console.log("Observer timed out after 10 seconds");
    }, 10000);

    console.log("We have finished addEventListenersToPickItems function");
    return itemsData;
}
