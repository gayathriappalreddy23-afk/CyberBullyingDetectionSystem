document.addEventListener('DOMContentLoaded', function () {
    const dashboardRoot = document.querySelector('.moderator-dashboard');
    const filterForm = document.getElementById('moderationFiltersForm');
    const resetFilter = document.getElementById('moderationFiltersReset');
    const confirmModal = document.getElementById('confirmationModal');
    const confirmModalTitle = document.getElementById('confirmationModalLabel');
    const confirmModalBody = document.getElementById('confirmationModalBody');
    const confirmModalAction = document.getElementById('confirmationConfirmButton');
    const chartCanvas = document.getElementById('moderationDetectionChart');
    let pendingAction = null;

    function parseNumber(value) {
        const parsed = Number(value);
        return Number.isFinite(parsed) ? parsed : 0;
    }

    function initChart() {
        if (!chartCanvas || !dashboardRoot) {
            return;
        }

        const safeCount = parseNumber(dashboardRoot.dataset.safeCount);
        const bullyingCount = parseNumber(dashboardRoot.dataset.bullyingCount);
        const underReviewCount = parseNumber(dashboardRoot.dataset.underReviewCount);
        const data = [safeCount, bullyingCount, underReviewCount];
        const total = data.reduce((sum, value) => sum + value, 0);
        const chartData = total > 0 ? data : [1, 1, 1];

        new Chart(chartCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Safe Content', 'Cyberbullying', 'Under Review'],
                datasets: [{
                    data: chartData,
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
                                const value = context.formattedValue || 0;
                                return `${context.label}: ${value}`;
                            }
                        }
                    }
                }
            }
        });
    }

    function resetFilters(event) {
        event.preventDefault();
        if (!filterForm) {
            return;
        }
        filterForm.reset();
    }

    function openConfirmationModal(event) {
        const button = event.currentTarget;
        const actionLabel = button.dataset.actionLabel || 'Confirm action';
        const itemLabel = button.dataset.itemLabel || 'this item';
        pendingAction = {
            type: button.dataset.actionType || 'moderation',
            item: itemLabel
        };

        if (confirmModalTitle) {
            confirmModalTitle.textContent = `${actionLabel}`;
        }
        if (confirmModalBody) {
            confirmModalBody.textContent = `Are you sure you want to ${actionLabel.toLowerCase()} for ${itemLabel}? The backend must handle the secure moderation action.`;
        }
        if (confirmModalAction) {
            confirmModalAction.dataset.confirmType = pendingAction.type;
            confirmModalAction.dataset.confirmItem = pendingAction.item;
        }

        const modal = new bootstrap.Modal(confirmModal);
        modal.show();
    }

    function confirmAction(event) {
        event.preventDefault();
        if (!pendingAction) {
            return;
        }
        console.log('Confirmed moderation action:', pendingAction.type, pendingAction.item);
        if (confirmModal) {
            const modalInstance = bootstrap.Modal.getInstance(confirmModal);
            if (modalInstance) {
                modalInstance.hide();
            }
        }
    }

    function attachConfirmationTriggers() {
        const actionButtons = document.querySelectorAll('.confirm-action');
        actionButtons.forEach(function (button) {
            button.addEventListener('click', openConfirmationModal);
        });
    }

    if (resetFilter) {
        resetFilter.addEventListener('click', resetFilters);
    }

    if (confirmModalAction) {
        confirmModalAction.addEventListener('click', confirmAction);
    }

    initChart();
    attachConfirmationTriggers();
});
