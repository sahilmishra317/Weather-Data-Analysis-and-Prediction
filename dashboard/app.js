// Dashboard Application Logic

const COLORS = {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    tertiary: '#f43f5e',
    text: '#94a3b8',
    grid: 'rgba(255, 255, 255, 0.05)'
};

// Common Chart.js options for dark theme
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: { color: COLORS.text }
        }
    },
    scales: {
        x: {
            grid: { color: COLORS.grid },
            ticks: { color: COLORS.text }
        },
        y: {
            grid: { color: COLORS.grid },
            ticks: { color: COLORS.text }
        }
    }
};

async function initDashboard() {
    try {
        await loadCurrentWeather();
        await loadMonthlyAverages();
        await loadModelMetrics();
        await loadPredictions();
        animateCounters();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Fallback or demo data if pipeline hasn't run yet
    }
}

async function loadCurrentWeather() {
    try {
        const response = await fetch('../output/current_weather.json');
        if (!response.ok) throw new Error('Failed to load current weather');
        const data = await response.json();
        
        document.getElementById('current-temp').innerText = data.temperature.toFixed(1);
        document.getElementById('current-humidity').innerText = data.humidity.toFixed(0) + '%';
        document.getElementById('current-wind').innerText = data.wind_speed.toFixed(1) + ' km/h';
        document.getElementById('current-clouds').innerText = data.cloud_cover.toFixed(0) + '%';
        
        const dateObj = new Date(data.date);
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById('current-date-large').innerText = dateObj.toLocaleDateString('en-US', options);
    } catch (e) {
        console.error('Error fetching current weather:', e);
    }
}

async function loadMonthlyAverages() {
    const response = await fetch('../output/monthly_averages.json');
    if (!response.ok) throw new Error('Failed to load monthly averages');
    const data = await response.json();
    
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const values = Object.values(data);
    
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    
    // Create gradient
    let gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(244, 63, 94, 0.5)');   
    gradient.addColorStop(1, 'rgba(244, 63, 94, 0.0)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Avg Temperature (°C)',
                data: values,
                backgroundColor: gradient,
                borderColor: COLORS.tertiary,
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: commonOptions
    });
}

async function loadModelMetrics() {
    const response = await fetch('../output/model_metrics.json');
    if (!response.ok) throw new Error('Failed to load model metrics');
    const data = await response.json();
    
    const models = Object.keys(data);
    const mae = models.map(m => data[m].MAE);
    const rmse = models.map(m => data[m].RMSE);
    const r2 = models.map(m => data[m].R2);
    
    // Error Metrics Chart (Bar)
    const ctx1 = document.getElementById('metricsChart').getContext('2d');
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [
                {
                    label: 'MAE',
                    data: mae,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderRadius: 4
                },
                {
                    label: 'RMSE',
                    data: rmse,
                    backgroundColor: 'rgba(139, 92, 246, 0.7)',
                    borderRadius: 4
                }
            ]
        },
        options: commonOptions
    });
    
    // R2 Chart (Polar Area or Bar)
    const ctx2 = document.getElementById('r2Chart').getContext('2d');
    new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: models,
            datasets: [{
                label: 'R² Score',
                data: r2,
                backgroundColor: 'rgba(16, 185, 129, 0.7)',
                borderRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 1
                }
            }
        }
    });

    // Update 'Best Model' stat dynamically based on R2
    let bestModel = models[0];
    let maxR2 = data[bestModel].R2;
    for(let m of models) {
        if(data[m].R2 > maxR2) {
            maxR2 = data[m].R2;
            bestModel = m;
        }
    }
    // Set to DOM if needed, currently hardcoded in HTML as Random Forest.
}

async function loadPredictions() {
    const response = await fetch('../output/predictions.json');
    if (!response.ok) throw new Error('Failed to load predictions');
    const data = await response.json();
    
    // We'll show the next 365 days
    const dates = data.map(d => d.date);
    const temps = data.map(d => d.predicted_temp);
    
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    let gradient = ctx.createLinearGradient(0, 0, 0, 500);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');   
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Predicted Next Year Temp (°C)',
                data: temps,
                borderColor: COLORS.primary,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            ...commonOptions,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        color: COLORS.text,
                        maxTicksLimit: 12
                    }
                },
                y: {
                    grid: { color: COLORS.grid },
                    ticks: { color: COLORS.text }
                }
            }
        }
    });
}

function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    const speed = 200;

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(updateCount, 15);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', initDashboard);

// Smooth scrolling for navigation
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        // Only if it's a hash link
        if (this.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            document.querySelectorAll('nav li').forEach(li => li.classList.remove('active'));
            this.parentElement.classList.add('active');
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});
