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
    // Print message to the console
    console.log(`${packName} has been opened`);
  
    // Save the opened pack name in localStorage
    let openedPacks = JSON.parse(localStorage.getItem('openedPacks')) || [];
    if (!openedPacks.includes(packName)) {
      openedPacks.push(packName);
      localStorage.setItem('openedPacks', JSON.stringify(openedPacks));
    }

    // Wait for the pack animation to finish so that the pack contents are visible
    // waitForPackAnimation();
    
    const packItems = document.querySelectorAll('.entityContainer')
    console.log(`Pack Items Length: ${packItems.length}`);
    packItems.forEach(item => {
        // Extract the pack name from the closest `ut-store-pack-details-view` container
        const rating = item.querySelector('.rating').textContent;
        if (!rating){
            return
        } else {
            const name = item.querySelector('.name').textContent;
            const isTradeable = !item.closest('.untradeable');
            const isDuplicate = item.closest('.duplicate') ? true : false;
            
            const labels = item.querySelectorAll('.player-stats-data-component .label');

            let pacValue = null;
            let shoValue = null;
            let pasValue = null;
            let driValue = null;
            let defValue = null;
            let phyValue = null;

            labels.forEach(label => {
                const labelText = label.textContent.trim();
                switch (labelText) {
                    case 'PAC':
                        pacValue = label.nextElementSibling.textContent.trim();
                        break;
                    case 'SHO':
                        shoValue = label.nextElementSibling.textContent.trim();
                        break;
                    case 'PAS':
                        pasValue = label.nextElementSibling.textContent.trim();
                        break;
                    case 'DRI':
                        driValue = label.nextElementSibling.textContent.trim();
                        break;
                    case 'DEF':
                        defValue = label.nextElementSibling.textContent.trim();
                        break;
                    case 'PHY':
                        phyValue = label.nextElementSibling.textContent.trim();
                        break;
                }
            });

            console.log({
                name,
                rating,
                pac: pacValue,
                sho: shoValue,
                pas: pasValue,
                dri: driValue,
                def: defValue,
                phy: phyValue,
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

