/**
 * Theme toggling logic
 */
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('themeToggle');
    
    // Check if the toggle button exists on the page
    if (themeToggleBtn) {
        
        // Function to update the icon based on current theme
        const updateIcon = (theme) => {
            if (theme === 'dark') {
                themeToggleBtn.innerHTML = '☀️';
                themeToggleBtn.setAttribute('aria-label', 'Switch to light mode');
                themeToggleBtn.setAttribute('title', 'Switch to light mode');
            } else {
                themeToggleBtn.innerHTML = '🌙';
                themeToggleBtn.setAttribute('aria-label', 'Switch to dark mode');
                themeToggleBtn.setAttribute('title', 'Switch to dark mode');
            }
        };

        // Determine current theme (from data attribute set by head script)
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        updateIcon(currentTheme);

        // Add click listener
        themeToggleBtn.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            
            // Set the attribute
            if (newTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
            }
            
            // Save to local storage
            localStorage.setItem('theme', newTheme);
            
            // Update the icon
            updateIcon(newTheme);
        });
    }
});
