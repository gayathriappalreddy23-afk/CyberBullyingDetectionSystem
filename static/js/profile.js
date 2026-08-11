/**
 * CyberBullyingDetectionSystem - Profile Page JS (profile.js)
 * Provides UI enhancements and logout confirmation prompts.
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------------------
    // Logout Confirmation Dialog
    // -------------------------------------------------------------------------
    const logoutForm = document.getElementById('profileLogoutForm');
    if (logoutForm) {
        logoutForm.addEventListener('submit', function (e) {
            const confirmed = window.confirm('Are you sure you want to log out of your session?');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    }

    // -------------------------------------------------------------------------
    // Copy Username to Clipboard Helper
    // -------------------------------------------------------------------------
    const copyHandleBtn = document.getElementById('copyHandleBtn');
    if (copyHandleBtn) {
        copyHandleBtn.addEventListener('click', function () {
            const handleText = copyHandleBtn.getAttribute('data-handle') || '';
            if (handleText && navigator.clipboard) {
                navigator.clipboard.writeText(handleText).then(() => {
                    const originalHTML = copyHandleBtn.innerHTML;
                    copyHandleBtn.innerHTML = '<i class="bi bi-check2 text-success"></i> Copied!';
                    setTimeout(() => {
                        copyHandleBtn.innerHTML = originalHTML;
                    }, 2000);
                }).catch(() => {});
            }
        });
    }
});
