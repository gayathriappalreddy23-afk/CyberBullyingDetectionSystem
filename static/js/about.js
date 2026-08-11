/**
 * CyberBullyingDetectionSystem - About Page JavaScript (about.js)
 */

document.addEventListener('DOMContentLoaded', function () {
    // Smooth scrolling for anchor links if any on the about page
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetEl = document.querySelector(targetId);
                if (targetEl) {
                    e.preventDefault();
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
});
