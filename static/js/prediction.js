document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('detectionText');
    const counter = document.getElementById('textCounter');
    const submitButton = document.getElementById('detectSubmit');
    const clearButton = document.getElementById('detectClear');
    const form = document.getElementById('detectionForm');
    const feedback = document.getElementById('inputFeedback');
    const maxLength = Number(textarea?.getAttribute('maxlength')) || 1000;

    function updateCounter() {
        if (!textarea) {
            return;
        }

        const valueLength = textarea.value.length;
        if (counter) {
            counter.textContent = `${valueLength} / ${maxLength} characters`;
            if (valueLength >= maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        }

        if (submitButton) {
            submitButton.disabled = valueLength === 0;
        }
    }

    function resetForm() {
        if (!textarea) {
            return;
        }

        textarea.value = '';
        updateCounter();
        if (feedback) {
            feedback.textContent = '';
            feedback.classList.remove('text-danger');
        }
        if (submitButton) {
            submitButton.textContent = 'Detect Cyberbullying';
            submitButton.disabled = true;
        }
    }

    function validateInput() {
        if (!textarea) {
            return true;
        }

        const value = textarea.value || '';
        const trimmed = value.trim();

        if (!trimmed.length) {
            if (feedback) {
                feedback.textContent = 'Please enter some text to analyze.';
                feedback.classList.add('text-danger');
            }
            textarea.focus();
            return false;
        }

        if (trimmed.length > maxLength) {
            if (feedback) {
                feedback.textContent = `Text cannot exceed ${maxLength} characters.`;
                feedback.classList.add('text-danger');
            }
            textarea.focus();
            return false;
        }

        if (!/[A-Za-z0-9]/.test(trimmed)) {
            if (feedback) {
                feedback.textContent = 'Please enter meaningful text.';
                feedback.classList.add('text-danger');
            }
            textarea.focus();
            return false;
        }

        if (feedback) {
            feedback.textContent = '';
            feedback.classList.remove('text-danger');
        }
        return true;
    }

    function showLoadingState() {
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Analyzing...';
        }
    }

    if (textarea) {
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    if (clearButton) {
        clearButton.addEventListener('click', function (event) {
            event.preventDefault();
            resetForm();
        });
    }

    if (form) {
        form.addEventListener('submit', function (event) {
            if (!validateInput()) {
                event.preventDefault();
                return;
            }
            showLoadingState();
        });
    }

    const confidenceFill = document.querySelector('.confidence-fill');
    if (confidenceFill) {
        const targetConfidence = Number(confidenceFill.getAttribute('data-confidence')) || 0;
        const safeConfidence = Math.min(100, Math.max(0, targetConfidence));
        requestAnimationFrame(function () {
            confidenceFill.style.width = `${safeConfidence}%`;
        });
    }
});
