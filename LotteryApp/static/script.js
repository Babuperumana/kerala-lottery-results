// Frontend controller for Kerala Lottery Live Display

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const prizeNumberEl = document.getElementById('prize-number');
    const waitingSpinnerEl = document.getElementById('waiting-spinner');
    const updateTimeEl = document.getElementById('update-time');
    const countdownEl = document.getElementById('countdown');
    
    const activeLotteryEl = document.getElementById('active-lottery');
    const activeDateEl = document.getElementById('active-date');
    const historyGridEl = document.getElementById('history-grid');

    // State Variables
    let currentPrize = '';
    let countdownInterval = null;
    const REFRESH_INTERVAL_SEC = 30;
    let secondsLeft = REFRESH_INTERVAL_SEC;

    /**
     * Updates the countdown timer display and checks if we need to fetch.
     */
    function startCountdown() {
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
        
        secondsLeft = REFRESH_INTERVAL_SEC;
        countdownEl.textContent = secondsLeft;

        countdownInterval = setInterval(() => {
            secondsLeft--;
            countdownEl.textContent = secondsLeft;

            if (secondsLeft <= 0) {
                clearInterval(countdownInterval);
                fetchResult();
            }
        }, 1000);
    }

    /**
     * Fetches the latest result from the API endpoint.
     */
    async function fetchResult() {
        try {
            const response = await fetch('/api/result');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Process the result
            const newPrize = data.firstPrize || "Waiting for Live Result...";
            const updatedTime = data.updated || "Waiting...";
            const lotteryTitle = data.lottery || "Today's Draw";
            const drawDate = data.date || "";
            const history = data.history || [];
            
            updateUI(newPrize, updatedTime, lotteryTitle, drawDate, history);
            
        } catch (error) {
            console.error('Fetch error:', error);
            // Display error indicator without wiping out a successfully fetched prize number
            updateTimeEl.innerHTML = `<span style="color: #ff5e62;">Offline (Retrying...)</span>`;
        } finally {
            // Restart the countdown clock
            startCountdown();
        }
    }

    /**
     * Updates the UI elements with smooth transitions.
     * @param {string} newPrize The new prize text to display.
     * @param {string} updatedTime The update timestamp.
     * @param {string} lotteryTitle Today's draw name.
     * @param {string} drawDate Today's draw date.
     * @param {Array} history History draw items.
     */
    function updateUI(newPrize, updatedTime, lotteryTitle, drawDate, history) {
        // Update headers
        if (activeLotteryEl) activeLotteryEl.textContent = lotteryTitle;
        if (activeDateEl) {
            if (drawDate) {
                activeDateEl.textContent = drawDate;
                activeDateEl.style.display = 'inline-block';
            } else {
                activeDateEl.style.display = 'none';
            }
        }

        // Update timestamp
        updateTimeEl.textContent = updatedTime;

        // Render previous draws history list
        renderHistory(history);

        // If the prize number text is identical, skip transition animation to save rendering overhead
        if (currentPrize === newPrize) {
            return;
        }

        // Cache the new value
        currentPrize = newPrize;

        // Add class to trigger smooth CSS fade/blur out
        prizeNumberEl.classList.add('fade-out');

        // Wait for CSS transition (400ms) to complete before altering content
        setTimeout(() => {
            prizeNumberEl.textContent = newPrize;

            const isWaiting = newPrize === "Waiting for Live Result...";

            if (isWaiting) {
                // Change style state to waiting
                prizeNumberEl.className = 'prize-text state-waiting';
                // Show loading spinner
                waitingSpinnerEl.style.display = 'flex';
            } else {
                // Change style state to winner (neon gold glow)
                prizeNumberEl.className = 'prize-text state-winner';
                // Hide loading spinner
                waitingSpinnerEl.style.display = 'none';
            }

            // Remove class to fade back in smoothly
            prizeNumberEl.classList.remove('fade-out');
        }, 400);
    }

    /**
     * Renders the previous 3 draws dynamically inside the history section.
     * @param {Array} history 
     */
    function renderHistory(history) {
        if (!historyGridEl) return;
        historyGridEl.innerHTML = '';
        
        if (!history || history.length === 0) {
            historyGridEl.innerHTML = '<div class="history-placeholder">No draw history available</div>';
            return;
        }
        
        history.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-card';
            
            // Name (e.g. Bhagyathara)
            const nameEl = document.createElement('div');
            nameEl.className = 'history-card-name';
            nameEl.textContent = item.lottery;
            
            // Draw Code (e.g. BT-61)
            const codeEl = document.createElement('div');
            codeEl.className = 'history-card-code';
            codeEl.textContent = item.code || '';
            
            // 1st prize number
            const prizeEl = document.createElement('div');
            prizeEl.className = 'history-card-prize';
            prizeEl.textContent = item.firstPrize || 'Waiting...';
            
            // Date (e.g. 06-07-2026)
            const dateEl = document.createElement('div');
            dateEl.className = 'history-card-date';
            dateEl.textContent = item.date || '';
            
            card.appendChild(nameEl);
            if (item.code) card.appendChild(codeEl);
            card.appendChild(prizeEl);
            card.appendChild(dateEl);
            
            historyGridEl.appendChild(card);
        });
    }

    // Run immediate check upon loading
    fetchResult();
});
