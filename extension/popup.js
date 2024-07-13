document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.local.get('packData', (result) => {
        let packStats = result.packData || [];
        let packStatsDiv = document.getElementById('pack-stats');

        packStats.forEach(pack => {
            let packElement = document.createElement('div');
            packElement.textContent = `Pack: ${pack.name} - Value: ${pack.value}`;
            packStatsDiv.appendChild(packElement);
        });
    });
});
