/**
 * posts.js
 * Frontend logic for CyberBullyingDetectionSystem post creation and editing.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Selectors
    const postForm = document.getElementById('editPostForm') || document.getElementById('createPostForm');
    
    if (!postForm) return; // Exit if no post form is on page

    const titleInput = document.getElementById('id_title');
    const contentInput = document.getElementById('id_content');
    const categorySelect = document.getElementById('id_category');
    const imageInput = document.getElementById('id_image');
    const charCount = document.getElementById('charCount');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const previewBtn = document.getElementById('previewBtn');
    
    // Image preview selectors
    const newImagePreviewContainer = document.getElementById('newImagePreviewContainer');
    const newImagePreview = document.getElementById('newImagePreview');
    const clearNewImageBtn = document.getElementById('clearNewImageBtn');
    const imageError = document.getElementById('imageError');
    const imageClearCheckbox = document.getElementById('image-clear_id');
    
    // Constants
    const MAX_LENGTH = 2000;
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

    // Track original state for 'Unsaved Changes' and 'Reset' features
    const originalState = {
        title: titleInput ? titleInput.value : '',
        content: contentInput ? contentInput.value : '',
        category: categorySelect ? categorySelect.value : '',
        imageClearChecked: imageClearCheckbox ? imageClearCheckbox.checked : false
    };

    let formChanged = false;
    let isSubmitting = false;

    // --- 1. Character Counter ---
    if (contentInput && charCount) {
        const updateCharCount = () => {
            const currentLength = contentInput.value.length;
            charCount.textContent = currentLength;
            
            if (currentLength >= MAX_LENGTH * 0.9) {
                charCount.classList.add('text-warning');
                charCount.classList.remove('text-danger', 'text-muted');
            } else {
                charCount.classList.remove('text-warning', 'text-danger');
                charCount.classList.add('text-muted');
            }
            
            if (currentLength > MAX_LENGTH) {
                charCount.classList.add('text-danger');
                charCount.classList.remove('text-warning', 'text-muted');
            }
        };

        contentInput.addEventListener('input', updateCharCount);
        updateCharCount(); // Initialize
    }

    // --- 2. Change Tracking ---
    const markAsChanged = () => {
        formChanged = true;
    };

    if (titleInput) titleInput.addEventListener('input', markAsChanged);
    if (contentInput) contentInput.addEventListener('input', markAsChanged);
    if (categorySelect) categorySelect.addEventListener('change', markAsChanged);
    if (imageClearCheckbox) imageClearCheckbox.addEventListener('change', markAsChanged);

    // --- 3. Image Handling & Validation ---
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            markAsChanged();
            const file = this.files[0];
            
            // Reset error
            imageError.classList.add('d-none');
            imageError.textContent = '';
            
            if (file) {
                // Validate Type
                if (!ALLOWED_TYPES.includes(file.type)) {
                    showImageError('Invalid file type. Please upload a JPG, PNG, or WEBP image.');
                    this.value = ''; // Clear input
                    hideNewImagePreview();
                    return;
                }
                
                // Validate Size
                if (file.size > MAX_FILE_SIZE) {
                    showImageError('File is too large. Maximum size is 5MB.');
                    this.value = ''; // Clear input
                    hideNewImagePreview();
                    return;
                }

                // Show Preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    newImagePreview.src = e.target.result;
                    newImagePreviewContainer.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            } else {
                hideNewImagePreview();
            }
        });
    }

    if (clearNewImageBtn && imageInput) {
        clearNewImageBtn.addEventListener('click', function() {
            imageInput.value = '';
            hideNewImagePreview();
        });
    }

    function showImageError(msg) {
        imageError.textContent = msg;
        imageError.classList.remove('d-none');
    }

    function hideNewImagePreview() {
        newImagePreview.src = '#';
        newImagePreviewContainer.classList.add('d-none');
    }

    // --- 4. Preview Feature ---
    if (previewBtn) {
        previewBtn.addEventListener('click', function() {
            const previewTitle = document.getElementById('previewTitle');
            const previewContent = document.getElementById('previewContent');
            const previewCategory = document.getElementById('previewCategory');
            const previewImageWrapper = document.getElementById('previewImageWrapper');
            const previewModalImage = document.getElementById('previewModalImage');
            
            if (previewTitle) previewTitle.textContent = titleInput.value || 'Untitled Post';
            if (previewContent) previewContent.textContent = contentInput.value || 'No content written yet.';
            
            if (previewCategory && categorySelect) {
                const selectedOption = categorySelect.options[categorySelect.selectedIndex];
                previewCategory.textContent = selectedOption && selectedOption.value ? selectedOption.text : 'Uncategorized';
            }

            // Determine which image to show in preview
            let imageSource = null;
            
            if (imageInput && imageInput.files[0]) {
                // Show newly uploaded image
                imageSource = newImagePreview.src;
            } else if (imageClearCheckbox && imageClearCheckbox.checked) {
                // User explicitly requested to remove current image
                imageSource = null;
            } else {
                // Try to find current existing image
                const currentImg = document.querySelector('.img-preview-current');
                if (currentImg) {
                    imageSource = currentImg.src;
                }
            }

            if (imageSource && previewImageWrapper && previewModalImage) {
                previewModalImage.src = imageSource;
                previewImageWrapper.classList.remove('d-none');
            } else if (previewImageWrapper) {
                previewImageWrapper.classList.add('d-none');
            }
        });
    }

    // --- 5. Reset Changes ---
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to discard your unsaved changes?')) {
                if (titleInput) titleInput.value = originalState.title;
                if (contentInput) {
                    contentInput.value = originalState.content;
                    contentInput.dispatchEvent(new Event('input')); // Trigger char counter update
                }
                if (categorySelect) categorySelect.value = originalState.category;
                
                if (imageClearCheckbox) imageClearCheckbox.checked = originalState.imageClearChecked;
                if (imageInput) {
                    imageInput.value = '';
                    hideNewImagePreview();
                }
                
                // Clear validation states
                postForm.classList.remove('was-validated');
                
                formChanged = false;
            }
        });
    }

    // --- 6. Form Submission & Validation ---
    postForm.addEventListener('submit', function(e) {
        // Prevent submission if already submitting
        if (isSubmitting) {
            e.preventDefault();
            return;
        }

        // Bootstrap native validation check
        if (!postForm.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            postForm.classList.add('was-validated');
            
            // Find first invalid element and focus it
            const firstInvalid = postForm.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.focus();
            }
            return;
        }

        // Custom Validation: Empty spaces check for content
        if (contentInput && contentInput.value.trim() === '') {
            e.preventDefault();
            contentInput.setCustomValidity('Content cannot be only spaces.');
            postForm.classList.add('was-validated');
            contentInput.focus();
            return;
        } else if (contentInput) {
            contentInput.setCustomValidity('');
        }

        // UI Loading State
        isSubmitting = true;
        formChanged = false; // Bypass unsaved changes warning
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
        }
    });

    // --- 7. Unsaved Changes Warning ---
    window.addEventListener('beforeunload', function(e) {
        if (formChanged && !isSubmitting) {
            const confirmationMessage = 'You have unsaved changes. Are you sure you want to leave?';
            e.returnValue = confirmationMessage; // Gecko, Trident, Chrome 34+
            return confirmationMessage; // Gecko, WebKit, Chrome <34
        }
    });

    // --- 8. Post Detail Specific Logic ---
    const deletePostForms = document.querySelectorAll('.delete-post-form');
    if (deletePostForms.length > 0) {
        deletePostForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const isConfirmed = confirm("Are you sure you want to delete this post? This action cannot be undone.");
                
                if (!isConfirmed) {
                    e.preventDefault();
                } else {
                    const deleteBtn = form.querySelector('.delete-btn');
                    if (deleteBtn) {
                        deleteBtn.disabled = true;
                        deleteBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Deleting...';
                    }
                }
            });
        });
    }

    const commentFormInline = document.getElementById('commentFormInline');
    const commentContentInline = document.getElementById('commentContentInline');
    const charCountInline = document.getElementById('charCountInline');
    const submitCommentBtn = document.getElementById('submitCommentBtn');
    const commentErrorInline = document.getElementById('commentErrorInline');

    if (commentContentInline && charCountInline) {
        const updateInlineCharCount = () => {
            const currentLength = commentContentInline.value.length;
            charCountInline.textContent = currentLength;
            
            if (currentLength >= 500 * 0.9) {
                charCountInline.classList.add('text-warning');
                charCountInline.classList.remove('text-danger', 'text-muted');
            } else {
                charCountInline.classList.remove('text-warning', 'text-danger');
                charCountInline.classList.add('text-muted');
            }
            
            if (currentLength > 500) {
                charCountInline.classList.add('text-danger');
                charCountInline.classList.remove('text-warning', 'text-muted');
            }
            
            if (commentErrorInline.style.display === 'block') {
                commentErrorInline.style.display = 'none';
                commentContentInline.classList.remove('is-invalid');
            }
        };
        commentContentInline.addEventListener('input', updateInlineCharCount);
    }

    if (commentFormInline) {
        commentFormInline.addEventListener('submit', function(e) {
            const content = commentContentInline.value;
            
            if (!content || content.trim().length === 0) {
                e.preventDefault();
                commentErrorInline.textContent = "Comment cannot be empty or contain only spaces.";
                commentErrorInline.style.display = 'block';
                commentContentInline.classList.add('is-invalid');
                commentContentInline.focus();
                return;
            }

            if (content.length > 500) {
                e.preventDefault();
                commentErrorInline.textContent = "Comment exceeds maximum length.";
                commentErrorInline.style.display = 'block';
                commentContentInline.classList.add('is-invalid');
                return;
            }

            if (submitCommentBtn) {
                submitCommentBtn.disabled = true;
                submitCommentBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Posting...';
            }
        });
    }
});
