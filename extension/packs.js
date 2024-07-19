/**
 * addEventListenersToPacks will be triggered when ever a change in the DOM is detected
 * It will look for the presence of the Open button for packs
 * If packs are located on screen event listeners will be added to the Open button for each pack
 * Upon a click it will trigger the function handlePackOpened
 */
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
      
        //Extract the pack name
        const packNameElement = detailsView.querySelector('h1.ut-store-pack-details-view--title span');
        const packName = packNameElement ? packNameElement.textContent.trim() : 'Unknown Pack';
  
        // If no listener is added, mark the listener as added
        if (!button.dataset.listenerAdded) {
        button.dataset.listenerAdded = 'true';
  
        console.log(`Added an event listener to pack: ${packName}`);
        
        // Add event listener to the button
        button.addEventListener('click', () => {
            // Delay the execution by 5 seconds to allow pack opening animation to finish
            setTimeout(() => {
                handlePackOpened(packName); // Call the function to handle pack opening
            }, 5000); // 5000 milliseconds = 5 seconds
        });
      }
    });
  }


/**
 * This is triggered after a pack has been opened. It will iterate through each item in the pack and extract
 * the data for each item. The variable names are returned according to the column definitions that they represent
 * E.g. is_duplicate, is_tradeable, etc
 * Each item will be stored as an element of itemsData
 * The data is then sent to the backend via sendBatchDataToBackend
 * @param {String} packName : pack name that has been opened
 */
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

        let itemData = extractKeyPlayerAttributes(item, 'pack');
        // If no rating is returned then it is not a player and we dont want to track the data
        if (!itemData.rating) return;

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
    sendBatchDataToBackend({ pack_name: packName, items: itemsData }, 'http://localhost:8000/new_items/');
}