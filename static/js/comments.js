/**
 * comments.js
 * Frontend logic for the CyberBullyingDetectionSystem comments interface.
 */

document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('commentForm');
    const commentContent = document.getElementById('commentContent');
    const charCount = document.getElementById('charCount');
    const clearBtn = document.getElementById('clearBtn');
    const submitBtn = document.getElementById('submitBtn');
    const commentError = document.getElementById('commentError');
    const deleteForms = document.querySelectorAll('.delete-comment-form');

    const MAX_LENGTH = 500;

    if (commentContent) {
        // Update character count on input
        commentContent.addEventListener('input', function() {
            const currentLength = this.value.length;
            charCount.textContent = currentLength;
            
            // Visual feedback as user approaches limit
            if (currentLength >= MAX_LENGTH * 0.9) {
                charCount.classList.add('text-warning');
                charCount.classList.remove('text-danger');
            } else {
                charCount.classList.remove('text-warning', 'text-danger');
            }
            
            if (currentLength > MAX_LENGTH) {
                charCount.classList.add('text-danger');
                charCount.classList.remove('text-warning');
            }

            // Hide error if user starts typing again
            if (commentError.style.display === 'block') {
                commentError.style.display = 'none';
            }
        });

        // Clear button functionality
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                commentContent.value = '';
                charCount.textContent = '0';
                charCount.classList.remove('text-warning', 'text-danger');
                commentError.style.display = 'none';
                commentContent.focus();
            });
        }
    }

    // Form submission validation
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            const content = commentContent.value;
            
            // Validation 1: Empty or whitespace only
            if (!content || content.trim().length === 0) {
                e.preventDefault();
                showError("Comment cannot be empty or contain only spaces.");
                return;
            }

            // Validation 2: Max length
            if (content.length > MAX_LENGTH) {
                e.preventDefault();
                showError(`Comment exceeds the maximum allowed length of ${MAX_LENGTH} characters.`);
                return;
            }

            // UI loading state to prevent double submission
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Posting...';
            
            // Allow form to submit naturally to Django backend
        });
    }

    function showError(message) {
        if (commentError) {
            commentError.textContent = message;
            commentError.style.display = 'block';
            commentContent.focus();
        }
    }

    // Delete confirmation
    if (deleteForms.length > 0) {
        deleteForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const isConfirmed = confirm("Are you sure you want to delete this comment? This action cannot be undone.");
                
                if (!isConfirmed) {
                    e.preventDefault();
                } else {
                    // Disable button to prevent double click
                    const deleteBtn = form.querySelector('.delete-btn');
                    if (deleteBtn) {
                        deleteBtn.disabled = true;
                        deleteBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Deleting...';
                    }
                }
            });
        });
    }
});
