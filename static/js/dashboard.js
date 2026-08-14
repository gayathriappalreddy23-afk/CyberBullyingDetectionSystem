document.addEventListener('DOMContentLoaded', function () {
    // 1. NLP Keyword Orbit Interaction
    const keywords = document.querySelectorAll('.keyword');
    const inputBox = document.querySelector('.nlp-preview-text');
    const progressBar = document.querySelector('.nlp-progress-bar');
    const progressPercent = document.querySelector('.progress-percent');
    
    if (keywords.length && inputBox) {
        const originalText = inputBox.innerHTML;
        
        keywords.forEach(keyword => {
            keyword.addEventListener('mouseenter', function () {
                const text = this.querySelector('.keyword-text-wrapper').textContent.trim();
                const tooltip = this.getAttribute('data-tooltip') || '';
                inputBox.innerHTML = `<strong>Keyword Highlight:</strong> "${text}" &mdash; <span class="text-primary">${tooltip}</span>`;
                
                if (progressBar) {
                    progressBar.style.animationPlayState = 'paused';
                    progressBar.style.background = this.classList.contains('keyword-toxic') 
                        ? 'linear-gradient(90deg, #EF4444 0%, #F59E0B 100%)' 
                        : 'linear-gradient(90deg, #10B981 0%, #6EE7B7 100%)';
                }
            });
            
            keyword.addEventListener('mouseleave', function () {
                inputBox.innerHTML = originalText;
                if (progressBar) {
                    progressBar.style.animationPlayState = 'running';
                    progressBar.style.background = '';
                }
            });
        });
    }

    // 2. Chart.js Initialization for other dashboards
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

