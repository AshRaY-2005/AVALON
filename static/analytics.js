/**
 * AVALON Analytics Visualization Engine
 * Handles Chart.js initialization for 15+ high-impact metrics
 */

function initAnalytics(chartData) {
    // Set global Chart defaults for Premium Pastel Theme (Light Mode)
    Chart.defaults.color = '#636E72'; // Modern text muted
    Chart.defaults.borderColor = 'rgba(0, 0, 0, 0.05)';
    Chart.defaults.font.family = "'Outfit', sans-serif";

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: false, // Titles managed by card headers, but ready for direct use
                color: '#2D3436',
                font: { size: 16, weight: 'bold' }
            },
            legend: {
                position: 'bottom',
                labels: { padding: 20, usePointStyle: true, boxWidth: 10, font: { size: 12 } }
            },
            tooltip: {
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                titleColor: '#2D3436',
                bodyColor: '#636E72',
                borderColor: '#E9ECEF',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                boxPadding: 6
            }
        }
    };

    // 1. Progress Curve (Timeline)
    new Chart(document.getElementById('timelineChart'), {
        type: 'line',
        data: {
            labels: chartData.timeline.labels,
            datasets: [{
                label: 'Cumulative Progress %',
                data: chartData.timeline.progress,
                borderColor: '#10B981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 4,
                pointBackgroundColor: '#10B981',
                pointRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Completion %', font: { weight: 'bold' } }
                },
                x: {
                    title: { display: true, text: 'Project Phases', font: { weight: 'bold' } }
                }
            }
        }
    });

    // 2. Phase Cost Breakdown (Doughnut)
    new Chart(document.getElementById('phaseCostChart'), {
        type: 'doughnut',
        data: {
            labels: chartData.phase_costs.labels,
            datasets: [{
                data: chartData.phase_costs.data,
                backgroundColor: ['#7ED9C3', '#A0C4FF', '#FFD6A5', '#BDB2FF', '#CAFFBF', '#FFADAD'],
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverOffset: 25
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                legend: { position: 'right', labels: { padding: 15 } }
            }
        }
    });

    // 3. Resource Allocation (Bar)
    new Chart(document.getElementById('resourceChart'), {
        type: 'bar',
        data: {
            labels: chartData.resource_distribution.labels,
            datasets: [{
                label: 'Allocation (₹)',
                data: chartData.resource_distribution.data,
                backgroundColor: ['#7ED9C3', '#A0C4FF', '#FFD6A5', '#FFADAD'],
                borderRadius: 12,
                borderWidth: 1,
                borderColor: 'rgba(0,0,0,0.05)'
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: { title: { display: true, text: 'Cost (INR)', font: { weight: 'bold' } } }
            },
            plugins: { ...commonOptions.plugins, legend: { display: false } }
        }
    });

    // 4. Multi-Factor Risk Radar
    new Chart(document.getElementById('riskRadarChart'), {
        type: 'radar',
        data: {
            labels: chartData.risk_radar.labels,
            datasets: [{
                label: 'Severity (1-10)',
                data: chartData.risk_radar.data,
                backgroundColor: 'rgba(255, 173, 173, 0.3)',
                borderColor: '#FFADAD',
                pointBackgroundColor: '#FFADAD',
                borderWidth: 3,
                fill: true
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                r: {
                    angleLines: { display: true, color: 'rgba(0,0,0,0.1)' },
                    grid: { color: 'rgba(0,0,0,0.05)' },
                    suggestedMin: 0,
                    suggestedMax: 10,
                    ticks: { display: true, backdropColor: 'transparent', stepSize: 2 }
                }
            }
        }
    });

    // 5. Sustainability & ESG Index (Radar)
    new Chart(document.getElementById('sustainabilityChart'), {
        type: 'radar',
        data: {
            labels: chartData.sustainability_radar.labels,
            datasets: [{
                label: 'ESG Index',
                data: chartData.sustainability_radar.data,
                backgroundColor: 'rgba(202, 255, 191, 0.3)',
                borderColor: '#B0DF9D',
                pointBackgroundColor: '#B0DF9D',
                borderWidth: 3,
                fill: true
            }]
        },
        options: {
            ...commonOptions,
            scales: { r: { suggestedMin: 0, suggestedMax: 10, ticks: { display: false } } }
        }
    });

    // 6. Labor vs Material Cost Trend (Stacked Line)
    new Chart(document.getElementById('costDynamicsChart'), {
        type: 'line',
        data: {
            labels: chartData.labor_material_trend.labels,
            datasets: [
                {
                    label: 'Material Costs',
                    data: chartData.labor_material_trend.material,
                    borderColor: '#A0C4FF',
                    backgroundColor: 'rgba(160, 196, 255, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                },
                {
                    label: 'Labor Costs',
                    data: chartData.labor_material_trend.labor,
                    borderColor: '#7ED9C3',
                    backgroundColor: 'rgba(126, 217, 195, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                }
            ]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    stacked: true,
                    beginAtZero: true,
                    title: { display: true, text: 'Combined Cost (₹)', font: { weight: 'bold' } }
                }
            }
        }
    });

    // 7. Workforce Lifecycle (Area)
    new Chart(document.getElementById('workforceTrendChart'), {
        type: 'line',
        data: {
            labels: chartData.workforce_trends.labels,
            datasets: [{
                label: 'Workforce Size',
                data: chartData.workforce_trends.data,
                borderColor: '#BDB2FF',
                backgroundColor: 'rgba(189, 178, 255, 0.2)',
                fill: true,
                tension: 0.3,
                borderWidth: 3
            }]
        },
        options: {
            ...commonOptions,
            scales: { y: { title: { display: true, text: 'Headcount', font: { weight: 'bold' } } } }
        }
    });

    // 8. Material Consumption Intensity
    new Chart(document.getElementById('materialChart'), {
        type: 'polarArea',
        data: {
            labels: chartData.material_intensity.labels,
            datasets: [{
                data: chartData.material_intensity.data,
                backgroundColor: ['#A0C4FF', '#7ED9C3', '#FFD6A5', '#FFADAD', '#BDB2FF'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: commonOptions
    });

    // 9. Daily Burn Rate Trend
    new Chart(document.getElementById('burnRateChart'), {
        type: 'line',
        data: {
            labels: chartData.burn_rate_trend.labels,
            datasets: [{
                label: 'Daily Expenditure (₹)',
                data: chartData.burn_rate_trend.data,
                borderColor: '#FFD6A5',
                backgroundColor: 'rgba(255, 214, 165, 0.2)',
                tension: 0.4,
                pointRadius: 5,
                borderWidth: 3,
                pointBackgroundColor: '#FFD6A5'
            }]
        },
        options: {
            ...commonOptions,
            scales: { y: { title: { display: true, text: 'INR / Day', font: { weight: 'bold' } } } }
        }
    });

    // 10. Cost Scenario Variance
    new Chart(document.getElementById('varianceChart'), {
        type: 'bar',
        data: {
            labels: chartData.cost_variance.labels,
            datasets: [{
                label: 'Projected Total (₹)',
                data: chartData.cost_variance.data,
                backgroundColor: ['#7ED9C3', '#A0C4FF', '#FFADAD'],
                borderRadius: 12
            }]
        },
        options: {
            ...commonOptions,
            scales: { y: { title: { display: true, text: 'Total Estimate (₹)', font: { weight: 'bold' } } } },
            plugins: { ...commonOptions.plugins, legend: { display: false } }
        }
    });

    // 11. Phase Productivity Index
    new Chart(document.getElementById('productivityChart'), {
        type: 'bar',
        data: {
            labels: chartData.phase_productivity.labels,
            datasets: [{
                axis: 'y',
                label: 'Efficiency %',
                data: chartData.phase_productivity.data,
                backgroundColor: '#BDB2FF',
                borderRadius: 8
            }]
        },
        options: {
            ...commonOptions,
            indexAxis: 'y',
            scales: { x: { display: true, title: { display: true, text: 'Efficiency Rating' } } },
            plugins: { ...commonOptions.plugins, legend: { display: false } }
        }
    });

    // 12. Regulatory Complexity (Polar)
    new Chart(document.getElementById('regPolarChart'), {
        type: 'polarArea',
        data: {
            labels: chartData.regulatory_polar.labels,
            datasets: [{
                data: chartData.regulatory_polar.data,
                backgroundColor: ['#FFD6A5', '#CAFFBF', '#BDB2FF', '#7ED9C3', '#A0C4FF'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: commonOptions
    });

    // 13. Machinery Utilization (Bar)
    new Chart(document.getElementById('machineryChart'), {
        type: 'bar',
        data: {
            labels: chartData.machinery_efficiency.labels,
            datasets: [{
                label: 'Utilization %',
                data: chartData.machinery_efficiency.data,
                backgroundColor: '#A0C4FF',
                borderRadius: 10
            }]
        },
        options: {
            ...commonOptions,
            scales: { y: { title: { display: true, text: 'Utilization %', font: { weight: 'bold' } } } },
            plugins: { ...commonOptions.plugins, legend: { display: false } }
        }
    });
}
