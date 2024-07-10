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
    //   const uniqueId = detailsView.querySelector('h1.ut-store-pack-details-view--title span').textContent.trim() + button.outerHTML;
      
      // Check if the event listener is already added
      if (!button.dataset.listenerAdded) {
        button.dataset.listenerAdded = 'true'; // Mark as having the listener added
  
        // Print to console that the event listener was added
        console.log(`Added an event listener to pack: ${packName}`);
        
        // Add event listener to the button
        button.addEventListener('click', () => {
          handlePackOpened(packName); // Call the function to handle pack opening
        });
      }
    });
  }
  
  // Function to handle the logic when a pack is opened
  function handlePackOpened(packName) {
    // Print message to the console
    console.log(`${packName} has been opened`);
  
    // Save the opened pack name in localStorage
    let openedPacks = JSON.parse(localStorage.getItem('openedPacks')) || [];
    if (!openedPacks.includes(packName)) {
      openedPacks.push(packName);
      localStorage.setItem('openedPacks', JSON.stringify(openedPacks));
    }

    // Wait for the pack animation to finish so that the pack contents are visible
    waitForPackAnimation();
    
    const packItems = document.querySelectorAll('.entityContainer')
    packItems.forEach(item => {
        // Extract the pack name from the closest `ut-store-pack-details-view` container
        const rating = player.querySelector('.rating').textContent;
        if (!rating){
            return
        } else {
            const name = player.querySelector('.name').textContent;
            const pac = player.querySelector('.slot-position + ul .label[value="PAC"]').nextElementSibling.textContent;
            const sho = player.querySelector('.slot-position + ul .label[value="SHO"]').nextElementSibling.textContent;
            const pas = player.querySelector('.slot-position + ul .label[value="PAS"]').nextElementSibling.textContent;
            const dri = player.querySelector('.slot-position + ul .label[value="DRI"]').nextElementSibling.textContent;
            const def = player.querySelector('.slot-position + ul .label[value="DEF"]').nextElementSibling.textContent;
            const phy = player.querySelector('.slot-position + ul .label[value="PHY"]').nextElementSibling.textContent;
            const isTradeable = !player.closest('.untradeable');
            const isDuplicate = player.closest('.duplicate') ? true : false;
            
            console.log({
                name,
                rating,
                pac,
                sho,
                pas,
                dri,
                def,
                phy,
                isTradeable,
                isDuplicate
            });

        }

        
        
      });
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

