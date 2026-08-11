document.addEventListener('DOMContentLoaded', function () {
    const pageRoot = document.querySelector('.admin-dashboard');
    const detectionChartElement = document.getElementById('adminDetectionChart');
    const activityChartElement = document.getElementById('adminActivityChart');
    const resetButton = document.getElementById('adminFiltersReset');
    const filterForm = document.getElementById('adminFiltersForm');

    const parseNumber = (value) => {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
    };

    const initDetectionChart = function () {
        if (!detectionChartElement || !pageRoot) {
            return;
        }

        const safeCount = parseNumber(pageRoot.dataset.safeCount);
        const bullyingCount = parseNumber(pageRoot.dataset.bullyingCount);
        const underReviewCount = parseNumber(pageRoot.dataset.underReviewCount);
        const total = safeCount + bullyingCount + underReviewCount;
        const data = total > 0 ? [safeCount, bullyingCount, underReviewCount] : [1, 1, 1];

        new Chart(detectionChartElement, {
            type: 'doughnut',
            data: {
                labels: ['Safe Content', 'Cyberbullying', 'Under Review'],
                datasets: [{
                    data: data,
                    backgroundColor: ['#16A34A', '#DC2626', '#F59E0B'],
                    borderColor: '#FFFFFF',
                    borderWidth: 2,
                    hoverOffset: 6
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
    };

    const initActivityChart = function () {
        if (!activityChartElement || !pageRoot) {
            return;
        }

        const rawData = pageRoot.dataset.systemActivity || '[]';
        let activityData = [];

        try {
            activityData = JSON.parse(rawData);
        } catch (error) {
            activityData = [];
        }

        if (!Array.isArray(activityData) || activityData.length === 0) {
            return;
        }

        const labels = activityData.map((item) => item.label || 'N/A');
        const datasets = [
            {
                label: 'New Users',
                data: activityData.map((item) => parseNumber(item.new_users)),
                borderColor: '#2563EB',
                backgroundColor: 'rgba(37, 99, 235, 0.12)',
                fill: true,
                tension: 0.35
            },
            {
                label: 'Posts',
                data: activityData.map((item) => parseNumber(item.posts)),
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.12)',
                fill: true,
                tension: 0.35
            },
            {
                label: 'Comments',
                data: activityData.map((item) => parseNumber(item.comments)),
                borderColor: '#16A34A',
                backgroundColor: 'rgba(22, 163, 74, 0.12)',
                fill: true,
                tension: 0.35
            },
            {
                label: 'Reports',
                data: activityData.map((item) => parseNumber(item.reports)),
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.12)',
                fill: true,
                tension: 0.35
            },
            {
                label: 'Cyberbullying Detections',
                data: activityData.map((item) => parseNumber(item.bullying_detections)),
                borderColor: '#DC2626',
                backgroundColor: 'rgba(220, 38, 38, 0.12)',
                fill: true,
                tension: 0.35
            }
        ];

        new Chart(activityChartElement, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#475569'
                        },
                        grid: {
                            color: 'rgba(226, 232, 240, 0.65)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#475569'
                        },
                        grid: {
                            color: 'rgba(226, 232, 240, 0.65)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#1E293B'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `${context.dataset.label}: ${context.formattedValue}`;
                            }
                        }
                    }
                }
            }
        });
    };

    if (resetButton && filterForm) {
        resetButton.addEventListener('click', function (event) {
            event.preventDefault();
            filterForm.reset();
        });
    }

    initDetectionChart();
    initActivityChart();
});
