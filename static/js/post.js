/**
 * CyberBullyingDetectionSystem - Posts JS (post.js)
 * Enhances post creation & editing forms with character counting, UI loading state,
 * and unsaved changes confirmation warnings.
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------------------
    // 1. Dynamic Character Counter
    // -------------------------------------------------------------------------
    function setupCharCounter(inputId, counterId, maxLen) {
        const inputElem = document.getElementById(inputId);
        const counterElem = document.getElementById(counterId);

        if (!inputElem || !counterElem) return;

        function updateCount() {
            const currentLen = inputElem.value.length;
            counterElem.textContent = `${currentLen} / ${maxLen}`;

            if (currentLen >= maxLen) {
                counterElem.className = 'char-counter at-limit';
            } else if (currentLen >= maxLen * 0.85) {
                counterElem.className = 'char-counter near-limit';
            } else {
                counterElem.className = 'char-counter';
            }
        }

        inputElem.addEventListener('input', updateCount);
        updateCount(); // Initial count
    }

    setupCharCounter('id_title', 'titleCharCounter', 200);

    // -------------------------------------------------------------------------
    // 2. Submit Loading State
    // -------------------------------------------------------------------------
    const createPostForm = document.getElementById('createPostForm');
    const submitBtn = document.getElementById('publishPostSubmitBtn');

    let formIsSubmitting = false;

    if (createPostForm && submitBtn) {
        createPostForm.addEventListener('submit', function () {
            formIsSubmitting = true;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Publishing Post...';
        });
    }

    // -------------------------------------------------------------------------
    // 3. Unsaved Changes Guard
    // -------------------------------------------------------------------------
    const titleInput = document.getElementById('id_title');
    const contentInput = document.getElementById('id_content');

    window.addEventListener('beforeunload', function (e) {
        if (formIsSubmitting) return;

        const hasTitle = titleInput && titleInput.value.trim().length > 0;
        const hasContent = contentInput && contentInput.value.trim().length > 0;

        if (hasTitle || hasContent) {
            e.preventDefault();
            e.returnValue = ''; // Standard browser confirmation prompt
        }
    });
});
