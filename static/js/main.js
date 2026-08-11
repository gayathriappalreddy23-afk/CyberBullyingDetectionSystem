/**
 * CyberBullyingDetectionSystem - Global JavaScript (main.js)
 * Core interactive scripts for layout, sidebar toggle, auto-dismissing alerts, and tooltips.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Sidebar Toggle Functionality
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const sidebarWrapper = document.getElementById('sidebarWrapper');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        if (sidebarWrapper) {
            sidebarWrapper.classList.toggle('show');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle('show');
        }
    }

    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

    // Close sidebar when pressing ESC on mobile
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebarWrapper && sidebarWrapper.classList.contains('show')) {
            toggleSidebar();
        }
    });

    // 2. Initialize Bootstrap Tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 3. Auto-dismiss alerts after 6 seconds if marked auto-dismissible
    const autoDismissAlerts = document.querySelectorAll('.alert-dismissible.auto-dismiss');
    autoDismissAlerts.forEach(function (alertEl) {
        setTimeout(function () {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
                if (bsAlert) bsAlert.close();
            } else {
                alertEl.style.opacity = '0';
                setTimeout(() => alertEl.remove(), 300);
            }
        }, 6000);
    });
});
