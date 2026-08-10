document.addEventListener('DOMContentLoaded', function () {
    const chartCanvas = document.getElementById('detectionChart');

    if (!chartCanvas) {
        return;
    }

    const safeCount = Number(document.body.dataset.safeCount || 0);
    const bullyingCount = Number(document.body.dataset.bullyingCount || 0);
    const safeValue = Number.isFinite(safeCount) && safeCount > 0 ? safeCount : 0;
    const bullyingValue = Number.isFinite(bullyingCount) && bullyingCount > 0 ? bullyingCount : 0;

    const total = safeValue + bullyingValue;
    const chartData = total > 0 ? [safeValue, bullyingValue] : [1, 1];

    new Chart(chartCanvas, {
        type: 'doughnut',
        data: {
            labels: ['Safe Content', 'Cyberbullying Content'],
            datasets: [{
                data: chartData,
                backgroundColor: ['#16A34A', '#DC2626'],
                borderColor: ['#FFFFFF', '#FFFFFF'],
                hoverOffset: 6,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#1E293B',
                        usePointStyle: true,
                        padding: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.formattedValue}`;
                        }
                    }
                }
            }
        }
    });
});
