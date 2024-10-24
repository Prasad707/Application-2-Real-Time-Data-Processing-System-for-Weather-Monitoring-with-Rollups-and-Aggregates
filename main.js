document.addEventListener('DOMContentLoaded', function() {
    fetchWeatherData();

    // Event listener for setting alert threshold
    document.getElementById('alert-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const threshold = document.getElementById('threshold').value;
        if (threshold) {
            setAlertThreshold(threshold);
        }
    });
});

// Fetch weather data from backend
function fetchWeatherData() {
    fetch('/api/weather')
        .then(response => response.json())
        .then(data => {
            const weatherList = document.getElementById('weather-list');
            weatherList.innerHTML = '';  // Clear the current content

            data.forEach(cityWeather => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <h3>${cityWeather.city}</h3>
                    <p>Temperature: ${cityWeather.temp.toFixed(2)}°C</p>
                    <p>Condition: ${cityWeather.condition}</p>
                `;
                weatherList.appendChild(li);
            });
        });
}

// Set alert threshold for temperature
function setAlertThreshold(threshold) {
    fetch('/api/set_alert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ threshold: threshold })
    })
    .then(response => response.json())
    .then(data => {
        alert('Alert threshold set to ' + threshold + '°C');
    });
}
