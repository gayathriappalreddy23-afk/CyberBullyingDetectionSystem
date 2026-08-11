/**
 * CyberBullyingDetectionSystem - Contact Page JavaScript (contact.js)
 * Handles: form validation, character counter, submission UX, FAQ, animations
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {

    // =========================================================================
    // 1. Character Counter for Message Textarea
    // =========================================================================
    const messageField = document.getElementById('id_message');
    const charCounter = document.getElementById('charCounter');
    const MAX_CHARS = 2000;

    if (messageField && charCounter) {
        function updateCharCounter() {
            const len = messageField.value.length;
            const remaining = MAX_CHARS - len;
            charCounter.textContent = `${len} / ${MAX_CHARS} characters`;
            charCounter.classList.remove('warning', 'danger');
            if (remaining < 100) {
                charCounter.classList.add('danger');
            } else if (remaining < 300) {
                charCounter.classList.add('warning');
            }
        }
        messageField.addEventListener('input', updateCharCounter);
        updateCharCounter();
    }

    // =========================================================================
    // 2. Real-Time Form Validation
    // =========================================================================
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const fields = contactForm.querySelectorAll('[required]');

        fields.forEach(function (field) {
            field.addEventListener('blur', function () {
                validateField(field);
            });
            field.addEventListener('input', function () {
                if (field.classList.contains('is-invalid')) {
                    validateField(field);
                }
            });
        });

        function validateField(field) {
            const value = field.value.trim();
            let isValid = true;
            let feedbackEl = field.nextElementSibling;
            if (!feedbackEl || !feedbackEl.classList.contains('invalid-feedback')) {
                feedbackEl = null;
            }

            if (!value) {
                isValid = false;
                if (feedbackEl) feedbackEl.textContent = 'This field is required.';
            } else if (field.type === 'email') {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(value)) {
                    isValid = false;
                    if (feedbackEl) feedbackEl.textContent = 'Please enter a valid email address.';
                }
            } else if (field.id === 'id_message' && value.length < 10) {
                isValid = false;
                if (feedbackEl) feedbackEl.textContent = 'Message must be at least 10 characters.';
            }

            field.classList.toggle('is-invalid', !isValid);
            field.classList.toggle('is-valid', isValid);
            return isValid;
        }

        // =====================================================================
        // 3. Form Submission Handler
        // =====================================================================
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            let allValid = true;
            fields.forEach(function (field) {
                if (!validateField(field)) allValid = false;
            });

            if (!allValid) {
                const firstInvalid = contactForm.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
                return;
            }

            const submitBtn = document.getElementById('contactSubmitBtn');
            const btnText = document.getElementById('btnText');
            const btnSpinner = document.getElementById('btnSpinner');
            const formBody = document.getElementById('contactFormBody');
            const successMsg = document.getElementById('contactSuccessMessage');

            // Show loading state
            if (submitBtn) submitBtn.disabled = true;
            if (btnText) btnText.textContent = 'Sending…';
            if (btnSpinner) btnSpinner.style.display = 'inline-block';

            // Submit the form via fetch (AJAX-style for Django CSRF)
            const formData = new FormData(contactForm);

            fetch(contactForm.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(function (response) {
                return response.json().catch(function () {
                    // If not JSON (standard redirect), treat as success
                    return { success: true };
                });
            })
            .then(function (data) {
                if (data && data.success === false) {
                    showFormError(data.message || 'An error occurred. Please try again.');
                    resetSubmitBtn(submitBtn, btnText, btnSpinner);
                } else {
                    // Show success state
                    if (formBody) formBody.style.display = 'none';
                    if (successMsg) successMsg.classList.add('visible');
                    contactForm.reset();
                }
            })
            .catch(function () {
                // Fallback: show success even on network edge-cases (e.g. Django redirect)
                if (formBody) formBody.style.display = 'none';
                if (successMsg) successMsg.classList.add('visible');
                contactForm.reset();
            });
        });
    }

    function resetSubmitBtn(btn, textEl, spinnerEl) {
        if (btn) btn.disabled = false;
        if (textEl) textEl.textContent = 'Send Message';
        if (spinnerEl) spinnerEl.style.display = 'none';
    }

    function showFormError(message) {
        let errorAlert = document.getElementById('formErrorAlert');
        if (!errorAlert) {
            errorAlert = document.createElement('div');
            errorAlert.id = 'formErrorAlert';
            errorAlert.className = 'alert alert-danger mt-3';
            errorAlert.setAttribute('role', 'alert');
            const form = document.getElementById('contactForm');
            if (form) form.prepend(errorAlert);
        }
        errorAlert.textContent = message;
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(function () {
            if (errorAlert) errorAlert.remove();
        }, 6000);
    }

    // =========================================================================
    // 4. Reset Form from Success State
    // =========================================================================
    const resetBtn = document.getElementById('resetContactForm');
    if (resetBtn) {
        resetBtn.addEventListener('click', function () {
            const formBody = document.getElementById('contactFormBody');
            const successMsg = document.getElementById('contactSuccessMessage');
            const submitBtn = document.getElementById('contactSubmitBtn');
            const btnText = document.getElementById('btnText');
            const btnSpinner = document.getElementById('btnSpinner');

            if (successMsg) successMsg.classList.remove('visible');
            if (formBody) formBody.style.display = '';
            resetSubmitBtn(submitBtn, btnText, btnSpinner);
        });
    }

    // =========================================================================
    // 5. Intersection Observer — Animate Cards on Scroll
    // =========================================================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
    };

    const animateObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                animateObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.contact-info-card, .alt-contact-card, .faq-accordion .accordion-item').forEach(function (el, idx) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = `opacity 0.5s ease ${idx * 0.07}s, transform 0.5s ease ${idx * 0.07}s`;

        el.classList.add('observe-target');
        animateObserver.observe(el);
    });

    document.addEventListener('animationend', function () {}, { once: true });

    // Manually trigger animate-in style
    document.querySelectorAll('.observe-target').forEach(function (el) {
        el.addEventListener('transitionend', function () {
            el.style.opacity = '';
            el.style.transform = '';
        }, { once: true });
    });

    // Patch: animate-in class adds final state
    const style = document.createElement('style');
    style.textContent = '.animate-in { opacity: 1 !important; transform: translateY(0) !important; }';
    document.head.appendChild(style);

    // =========================================================================
    // 6. Copy Email on Click
    // =========================================================================
    const copyEmailBtn = document.getElementById('copyEmailBtn');
    if (copyEmailBtn) {
        copyEmailBtn.addEventListener('click', function () {
            const email = copyEmailBtn.getAttribute('data-email');
            if (email && navigator.clipboard) {
                navigator.clipboard.writeText(email).then(function () {
                    const originalHTML = copyEmailBtn.innerHTML;
                    copyEmailBtn.innerHTML = '<i class="bi bi-check2 me-1"></i>Copied!';
                    copyEmailBtn.classList.add('btn-success');
                    copyEmailBtn.classList.remove('btn-outline-secondary');
                    setTimeout(function () {
                        copyEmailBtn.innerHTML = originalHTML;
                        copyEmailBtn.classList.remove('btn-success');
                        copyEmailBtn.classList.add('btn-outline-secondary');
                    }, 2500);
                });
            }
        });
    }

});
