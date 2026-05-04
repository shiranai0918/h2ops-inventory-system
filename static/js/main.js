document.addEventListener('DOMContentLoaded', () => {
    // Dismiss flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.close-alert');
        if(closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.style.display = 'none';
            });
        }
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => { alert.style.display = 'none'; }, 300);
        }, 5000);
    });
});
