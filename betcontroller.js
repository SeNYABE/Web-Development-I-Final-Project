let form = document.getElementById('BetForm');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    let bet = document.getElementById('Bet').value;
    console.log("Bet placed:", bet);
    alert("Bet of " + bet + " placed successfully!");
});

// Fetch drivers and populate the betting selection
async function loadDrivers() {
    try {
        const response = await fetch('driverdb.json');
        const data = await response.json();
        const driversList = document.getElementById('drivers-list');
        
        if (!driversList) return;
        
        // Clear any existing content
        driversList.innerHTML = '';
        
        const drivers = data.drivers;
        
        // Generate a random odds number for demonstration purposes
        const generateOdds = () => {
            const isNegative = Math.random() > 0.5;
            const amount = Math.floor(Math.random() * 500) + 100;
            return isNegative ? `-${amount}` : `+${amount}`;
        };
        
        for (const [number, driver] of Object.entries(drivers)) {
            const card = document.createElement('div');
            card.className = 'feature-card';
            card.style.cursor = 'pointer'; 
            card.style.width = '250px'; 
            card.style.padding = '30px 20px';
            
            card.innerHTML = `
                <div class="icon" style="font-size: 2.5rem; margin-bottom: 10px;">🏎️</div>
                <h3 style="font-size: 1.2rem; margin-bottom: 5px;">${driver.name}</h3>
                <p style="color: var(--accent-color); font-weight: 800; font-size: 1.1rem; margin-bottom: 5px;">${driver.team}</p>
                <p style="font-size: 0.9rem; color: #666; margin-bottom: 15px;">#${number} | ${driver.nationality}</p>
                <p style="font-weight: 600; font-family: 'Outfit', sans-serif;">Odds: ${generateOdds()}</p>
            `;
            
            // Add click event to highlight the card and update the sidebar
            card.addEventListener('click', () => {
                // Reset all cards
                document.querySelectorAll('#drivers-list .feature-card').forEach(c => {
                    c.style.borderColor = 'rgba(0,0,0,0.05)';
                    c.style.transform = 'translateY(0)';
                    c.style.boxShadow = '0 10px 30px rgba(0,0,0,0.05)';
                });
                
                // Highlight selected card
                card.style.borderColor = 'var(--accent-color)';
                card.style.transform = 'translateY(-10px)';
                card.style.boxShadow = '0 20px 40px rgba(225, 6, 0, 0.2)';
                
                // Update sidebar info text
                const sidebarInfo = document.querySelector('.sidebar-info p');
                if (sidebarInfo) {
                    sidebarInfo.innerHTML = `You have selected <strong>${driver.name}</strong> from ${driver.team}. Enter your wager above to place the bet.`;
                }
            });
            
            driversList.appendChild(card);
        }
    } catch (error) {
        console.error("Error loading drivers:", error);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', loadDrivers);
