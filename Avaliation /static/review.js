document.querySelectorAll('.stars').forEach(starGroup => {
    const stars = starGroup.querySelectorAll('.fas');
    
    stars.forEach(star => {
        star.addEventListener('click', () => {
            const rating = parseInt(star.getAttribute('data-star'));
            
            // Update the hidden input field for this star group
            const ratingInput = starGroup.querySelector('input[type="hidden"]');
            ratingInput.value = rating;
            
            // Remove 'checked' class from stars in the current group
            starGroup.querySelectorAll('.fas').forEach(s => s.classList.remove('checked'));
            
            // Add 'checked' class to the selected star
            star.classList.add('checked');
        });
    });
});
