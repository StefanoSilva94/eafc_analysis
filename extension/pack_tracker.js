function addEventListenersToPicks() {
    // Select all buttons and find the one with the specific text
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
                // Delay the execution of handlePickOpened by 1 second
                setTimeout(() => {
                    handlePickOpened(pickName); // Call the function to handle pack opening
                }, 1000); // 1000 milliseconds = 1 second
            });

            // return True
        }
    } 
}

function addEventListenersToPickItems(itemsData, pickItems) {
    itemsData.forEach((item, idx) => {
        item.is_selected = (idx === 0); // First item is true, others are false
    });
    
    // Add event listeners to the items of the player pick to see which one is selected
    pickItems.forEach((pick, index) => {
        if (!pick.dataset.listenerAdded) {
            pick.dataset.listenerAdded = 'true';
      
            console.log(`Added an event listener to player: ${pick.querySelector('.name')?.textContent.trim()}`);
            
            // Add event listener to the pick item
            pick.addEventListener('click', () => {
                // update isSelected values
                const activePlayer = extractKeyPlayerAttributes(pick, 'pick');
                itemsData.forEach((item, idx) => {
                    item.is_selected = (index === idx);
                });

                console.log(`Updated items data:`, itemsData);
            });
        }
    });

    // Add event listeners to Confirm button
    const confirmButton = document.querySelector('.btn-standard.call-to-action');
    confirmButton.addEventListener('click', () => {
        // Print itemsData
        console.log('Final ITEMS DATA:', itemsData);
    });

    return itemsData;
}

function addEventListenersToPacks() {
    // Get all Open buttons on the page
    const openButtons = document.querySelectorAll('button.currency.call-to-action');
  
    openButtons.forEach(button => {
      // Extract the pack name from the closest `ut-store-pack-details-view` container
      const detailsView = button.closest('.ut-store-pack-details-view');
      if (!detailsView) {
        console.log("no details view for this button")
        return; 
      }
  
      const packNameElement = detailsView.querySelector('h1.ut-store-pack-details-view--title span');
      const packName = packNameElement ? packNameElement.textContent.trim() : 'Unknown Pack';
  
      
      // If no listener is added, mark the listener as added
      if (!button.dataset.listenerAdded) {
        button.dataset.listenerAdded = 'true';
  
        console.log(`Added an event listener to pack: ${packName}`);
        
        // Add event listener to the button
        button.addEventListener('click', () => {
            // Delay the execution of handlePackOpened by 5 seconds
            setTimeout(() => {
                handlePackOpened(packName); // Call the function to handle pack opening
            }, 7000); // 5000 milliseconds = 5 seconds
        });
      }
    });
  }
  
  // Function to handle the logic when a pack is opened
  function handlePackOpened(packName) {
    console.log(`${packName} has been opened`);

    // Save the opened pack name in localStorage
    let openedPacks = JSON.parse(localStorage.getItem('openedPacks')) || [];
    if (!openedPacks.includes(packName)) {
        openedPacks.push(packName);
        localStorage.setItem('openedPacks', JSON.stringify(openedPacks));
    }

    // Wait for the pack animation to finish
    // waitForPackAnimation();

    const packItems = document.querySelectorAll('.entityContainer');
    console.log(`Pack Items Length: ${packItems.length}`);

    // Array to hold all item data
    let itemsData = [];

    packItems.forEach(item => {
        const rating = item.querySelector('.rating')?.textContent.trim();
        if (!rating) return;

        const name = item.querySelector('.name')?.textContent.trim();
        const position = item.querySelector('.position')?.textContent.trim();
        const isTradeable = !item.querySelector('.untradeable');

        // Determine if item is a duplicate
        const headerElement = item.closest('.sectioned-item-list');
        const titleElement = headerElement?.querySelector('.title');
        const isDuplicate = titleElement?.textContent.trim() === 'Duplicates';

        // Initialize item object
        let itemData = {
            pack_name: packName,
            name,
            rating,
            position,
            is_tradeable: isTradeable,
            is_duplicate: isDuplicate
        };

        // Populate attributes based on player position
        if (position === "GK") {
            itemData = { ...itemData, ...extractGoalkeeperAttributes(item) };
        } else {
            itemData = { ...itemData, ...extractOutfieldPlayerAttributes(item) };
        }

        console.log("Item object:", itemData);
        console.log("JSON.stringify(item):", JSON.stringify(itemData));

        // Add item to itemsData array
        itemsData.push(itemData);
    });

    // Send the array of items to the backend
    sendBatchDataToBackend({ pack_name: packName, items: itemsData });
}

function handlePickOpened(pickName) {
    // Store each pick in pickItems
    // Iterate through each pick and store the data of each pick
    // Add a click event for each pick and for the Confirm button
    // If click is selected on Pick, update isSelected value for each item
    // Else confrim is clicked, send data to database

    console.log(`Player Pick: ${pickName} has been opened`);
    
    const pickItems = document.querySelectorAll(".player-pick-option");
    console.log(`Pick Items Length: ${pickItems.length}`);

    // Array to hold all item data
    let itemsData = [];

    pickItems.forEach(item => {
        // Get the players name, rating, position, isTradeable, isDuplicate
        let itemData = extractKeyPlayerAttributes(item, 'pick');
        console.log(`Item key data:: ${itemData}`);
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
    itemsData = addEventListenersToPickItems(itemsData, pickItems)
    console.log('Item all data:', itemsData);

}

function updateActivePlayer(pickItems) {
    pickItems.forEach(pick => {
        activeElement = pick.querySelector('.player-pick-option.selected')
        if (activeElement) {
            return extractKeyPlayerAttributes(pick)
        }
    })
}


function extractKeyPlayerAttributes(item, type) {
    const rating = item.querySelector('.rating')?.textContent.trim();
    if (!rating) return null; // Return null if rating is not found

    const name = item.querySelector('.name')?.textContent.trim();
    const position = item.querySelector('.position')?.textContent.trim();
    let isTradeable;
    let isDuplicate = false;
    
    if (type === 'pick') {
        const spanElements = item.querySelectorAll('span')
        spanElements.forEach(span => {
            if (span.textContent.trim() === 'Already Owned') {
                isDuplicate = true;
                return;
            }
        });
        isTradeable = false
    } else if (type === 'pack') {
        // Add logic for determining isDuplicate for packs if needed
        isDuplicate = false; // Default to false if no specific logic is provided
        isTradeable = !item.querySelector('.untradeable')
    }

    const itemData = {
        name,
        rating,
        position,
        is_tradeable: isTradeable,
        is_duplicate: isDuplicate,
    };

    return itemData;
}


function extractOutfieldPlayerAttributes(item) {
    const labels = item.querySelectorAll('.player-stats-data-component .label');
    const attributes = {
        pace: null,
        shooting: null,
        passing: null,
        dribbling: null,
        defending: null,
        physical: null
    };

    labels.forEach(label => {
        const labelText = label.textContent.trim();
        const value = label.nextElementSibling?.textContent.trim();
        switch (labelText) {
            case 'PAC':
                attributes.pace = value;
                break;
            case 'SHO':
                attributes.shooting = value;
                break;
            case 'PAS':
                attributes.passing = value;
                break;
            case 'DRI':
                attributes.dribbling = value;
                break;
            case 'DEF':
                attributes.defending = value;
                break;
            case 'PHY':
                attributes.physical = value;
                break;
        }
    });

    return attributes;
}

function extractGoalkeeperAttributes(item) {
    const labels = item.querySelectorAll('.player-stats-data-component .label');
    const attributes = {
        diving: null,
        handling: null,
        kicking: null,
        speed: null,
        reflexes: null,
        positioning: null
    };

    labels.forEach(label => {
        const labelText = label.textContent.trim();
        const value = label.nextElementSibling?.textContent.trim();
        switch (labelText) {
            case 'DIV':
                attributes.diving = value;
                break;
            case 'HAN':
                attributes.handling = value;
                break;
            case 'KIC':
                attributes.kicking = value;
                break;
            case 'SPD':
                attributes.speed = value;
                break;
            case 'REF':
                attributes.reflexes = value;
                break;
            case 'POS':
                attributes.positioning = value;
                break;
        }
    });

    return attributes;
}



function sendBatchDataToBackend(batchData) {
    fetch('http://localhost:8000/new_items/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(batchData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Batch data successfully sent to the backend:', data);
    })
    .catch((error) => {
        console.error('Error sending batch data to the backend:', error);
    });
}


async function sendDataToBackend(item) {
    // Log the item being sent to the backend
    console.log("Sending item to backend:", item);

    try {
        // Send the request
        const response = await fetch('http://localhost:8000/new_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(item)
        });

        // Check if the response is OK
        if (response.ok) {
            // Log successful response
            console.log("Data sent successfully!");
            
            // Optional: log the response body if needed
            const responseBody = await response.json();
            console.log("Response body:", responseBody);
        } else {
            // Log failed response status and text
            console.error("Failed to send data. Status:", response.status);
            console.error("Status Text:", response.statusText);

            // Optional: log the response body to get more details
            const responseBody = await response.text();
            console.error("Response body:", responseBody);
        }
    } catch (error) {
        // Log any errors encountered during the fetch
        console.error("Error sending data:", error);
    }
}
  
  
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
  
  // Initial call in case the elements are already present
//   addEventListenersToPacks();

