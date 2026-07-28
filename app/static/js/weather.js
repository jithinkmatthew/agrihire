tempChartInstance = null;

function renderWeatherChart() {

  siteLocation = document.getElementById('equipment_site_address');
  address = siteLocation.value

  let lat = null;
  let lon = null;

  const geocodingUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
  fetch(geocodingUrl)
    .then(response => response.json())
    .then(data => {
      console.log('data', data);
      if (data.length > 0) {
        lat = parseFloat(data[0].lat);
        lon = parseFloat(data[0].lon);


        const url = `/weather?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`;

        fetch(url)
          .then(response => response.json())
          .then(apiData => {
            const simplifiedData = {
              list: apiData.list.map(item => ({
                dt_txt: item.dt_txt,
                main: { temp: (item.main.temp - 273.15).toFixed(2) }
              }))
            };

            // Format dates into short readable strings
            const labels = simplifiedData.list.map(item => {
              const d = new Date(item.dt_txt);
              return d.toLocaleString('en-NZ', {
                day: 'numeric',    
                month: 'short',    
                hour: 'numeric',
                hour12: true
              });
            });

            // Extract temperatures
            const temps = simplifiedData.list.map(item => item.main.temp);

            if (tempChartInstance) {
              tempChartInstance.destroy();
            }

            // Build the chart
            tempChartInstance = new Chart(document.getElementById('tempChart'), {
              type: 'line',
              data: {
                labels: labels,
                datasets: [{
                  label: 'Temperature (°C)',
                  data: temps,
                  borderColor: 'rgba(75,192,192,1)',
                  backgroundColor: 'rgba(75,192,192,0.2)',
                  fill: true,
                  tension: 0.3
                }]
              },
              options: {
                responsive: true,
                plugins: {
                  legend: {
                    position: 'top'
                  },
                  tooltip: {
                    callbacks: {
                      label: function (context) {
                        return context.formattedValue + ' °C';
                      }
                    }
                  }
                },
                scales: {
                  x: {
                    type: 'category',
                    title: {
                      display: true,
                      text: 'Date & Time'
                    },
                    ticks: {
                      maxRotation: 60,
                      minRotation: 30
                    }
                  },
                  y: {
                    title: {
                      display: true,
                      text: 'Temperature (°C)'
                    }
                  }
                }
              }
            });
          })
      } else {
        alert('Location not found. Please try a different address.');
        const checkbox = document.getElementById("equipment_weather_forecast");
        checkbox.checked = false;
        return
      }
    })
    .catch(error => {
      console.error('Geocoding error:', error);
      alert('An error occurred during geocoding.');
    });
}

document.addEventListener('DOMContentLoaded', () => {
  const weatherCheckbox = document.getElementById('equipment_weather_forecast');
  const chart = document.getElementById('tempChart');
  
  chart.style.display = 'none';

  weatherCheckbox.addEventListener('change', () => {
    if (weatherCheckbox.checked) {
      chart.style.display = '';
      // Call chart rendering function only when checked
      renderWeatherChart(); 
    } else {
      chart.style.display = 'none';
    }
  });
});
