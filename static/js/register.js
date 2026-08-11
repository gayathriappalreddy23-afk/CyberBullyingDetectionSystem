/**
 * CyberBullyingDetectionSystem - Registration Page JS (register.js)
 * Enhances UI with accessible password visibility toggles and real-time visual strength hints.
 * Authoritative authentication & validation is strictly executed server-side by Django.
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------------------
    // 1. Password Visibility Toggle
    // -------------------------------------------------------------------------
    function setupPasswordToggle(toggleBtnId, targetInputId) {
        const toggleBtn = document.getElementById(toggleBtnId);
        const targetInput = document.getElementById(targetInputId);

        if (!toggleBtn || !targetInput) return;

        toggleBtn.addEventListener('click', function () {
            const isPassword = targetInput.type === 'password';
            targetInput.type = isPassword ? 'text' : 'password';

            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.className = isPassword ? 'bi bi-eye-slash' : 'bi bi-eye';
            }

            const labelText = isPassword ? 'Hide password' : 'Show password';
            toggleBtn.setAttribute('aria-label', labelText);
            toggleBtn.setAttribute('title', labelText);
        });
    }

    setupPasswordToggle('togglePassword1Btn', 'id_password1');
    setupPasswordToggle('togglePassword2Btn', 'id_password2');

    // -------------------------------------------------------------------------
    // 2. Real-time UX Password Strength Visualizer (Visual Hint Only)
    // -------------------------------------------------------------------------
    const passwordInput = document.getElementById('id_password1');
    const strengthProgress = document.getElementById('strengthProgress');
    const strengthText = document.getElementById('strengthText');

    if (passwordInput && strengthProgress && strengthText) {
        passwordInput.addEventListener('input', function () {
            const val = passwordInput.value;

            if (!val) {
                strengthProgress.className = 'password-strength-progress';
                strengthText.textContent = '';
                return;
            }

            let score = 0;
            if (val.length >= 8) score++;
            if (/[A-Z]/.test(val) || /[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val) && val.length >= 10) score++;

            if (score <= 1) {
                strengthProgress.className = 'password-strength-progress strength-weak';
                strengthText.textContent = 'Password strength: Weak';
                strengthText.style.color = '#DC2626';
            } else if (score === 2) {
                strengthProgress.className = 'password-strength-progress strength-medium';
                strengthText.textContent = 'Password strength: Medium';
                strengthText.style.color = '#D97706';
            } else {
                strengthProgress.className = 'password-strength-progress strength-strong';
                strengthText.textContent = 'Password strength: Strong';
                strengthText.style.color = '#16A34A';
            }
        });
    }

    // -------------------------------------------------------------------------
    // 3. Form Submit Button Loading State
    // -------------------------------------------------------------------------
    const registerForm = document.getElementById('registerForm');
    const submitBtn = document.getElementById('registerSubmitBtn');

    if (registerForm && submitBtn) {
        registerForm.addEventListener('submit', function () {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Creating Account...';
        });
    }
});
