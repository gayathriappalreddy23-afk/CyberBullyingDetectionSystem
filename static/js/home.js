/**
 * CyberBullyingDetectionSystem - Landing Page JavaScript (home.js)
 * Clean, lightweight script for smooth scroll interactions and UI enhancements.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Smooth Scroll for Learn More Anchor link
    const learnMoreBtn = document.querySelector('a[href="#problem-section"]');
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const targetSection = document.getElementById('problem-section');
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
});
