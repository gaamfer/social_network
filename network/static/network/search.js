document.addEventListener('DOMContentLoaded', function() {
    const area = document.querySelector('#search-area');
    const lupa = document.querySelector('#search-area-button');
    const leftarrow = document.querySelector('#search-area-left');

    if (area && lupa) {
        const HideShow = () => {
            area.style.display = area.style.display === 'none' ? 'block' : 'none';
            lupa.style.display = lupa.style.display === 'none' ? 'block' : 'none';
        };

        lupa.addEventListener('click', HideShow);
        leftarrow.addEventListener('click', HideShow);
        
    }
});