document.addEventListener('DOMContentLoaded', () => {
    // Sales Overview Chart
    const ctxOverview = document.getElementById('salesOverviewChart');
    if (ctxOverview) {
        fetch('/api/dashboard_data')
            .then(res => res.json())
            .then(data => {
                new Chart(ctxOverview, {
                    type: 'line',
                    data: {
                        labels: data.sales_overview.labels,
                        datasets: [{
                            label: 'Daily Revenue',
                            data: data.sales_overview.data,
                            borderColor: '#0A58CA',
                            backgroundColor: 'rgba(10, 88, 202, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true } }
                    }
                });
            });
    }

    // Forecasting Chart
    const ctxForecast = document.getElementById('forecastChart');
    if (ctxForecast) {
        fetch('/reports/api/forecasting_data')
            .then(res => res.json())
            .then(data => {
                new Chart(ctxForecast, {
                    type: 'line',
                    data: {
                        // For simplicity on dashboard, combine last 7 historical and next 7 forecast
                        labels: [...data.historical.labels.slice(-7), ...data.forecast.labels],
                        datasets: [
                            {
                                label: 'Historical',
                                data: [...data.historical.data.slice(-7), ...Array(7).fill(null)],
                                borderColor: '#0dcaf0',
                                backgroundColor: 'transparent',
                                borderWidth: 2,
                                tension: 0.1
                            },
                            {
                                label: 'Forecast',
                                data: [...Array(7).fill(null).map((_, i) => i === 6 ? data.historical.data[data.historical.data.length - 1] : null), ...data.forecast.data],
                                borderColor: '#ffc107',
                                backgroundColor: 'transparent',
                                borderDash: [5, 5],
                                borderWidth: 2,
                                tension: 0.1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: { y: { beginAtZero: true } }
                    }
                });
            });
    }
});
