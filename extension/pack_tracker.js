function addEventListenersToPacks() {
    // Get all Open buttons on the page
    const openButtons = document.querySelectorAll('button.currency.call-to-action');
    console.log(`Open buttons has ${openButtons.length} elements`);

  
    openButtons.forEach(button => {
      // Extract the pack name from the closest `ut-store-pack-details-view` container
      const detailsView = button.closest('.ut-store-pack-details-view');
      if (!detailsView) {
        console.log("no details view for this button")
        return; 
      }
  
      const packNameElement = detailsView.querySelector('h1.ut-store-pack-details-view--title span');
      const packName = packNameElement ? packNameElement.textContent.trim() : 'Unknown Pack';
  
      // Use a unique identifier for each pack to ensure listeners are only added once
      
      // Check if the event listener is already added
      if (!button.dataset.listenerAdded) {
        button.dataset.listenerAdded = 'true'; // Mark as having the listener added
  
        // Print to console that the event listener was added
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
        const is_tradeable = !item.querySelector('.untradeable');

        // Determine if item is a duplicate
        const headerElement = item.closest('.sectioned-item-list');
        const titleElement = headerElement?.querySelector('.title');
        const is_duplicate = titleElement?.textContent.trim() === 'Duplicates';

        // Initialize item object
        let itemData = {
            pack_name: packName,
            name,
            rating,
            position,
            is_tradeable,
            is_duplicate
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
  const observer = new MutationObserver(() => {
    addEventListenersToPacks();
  });
  
  // Start observing the document body for changes
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Initial call in case the elements are already present
  addEventListenersToPacks();

