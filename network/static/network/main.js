import { generate_post } from './api.js';

document.addEventListener('DOMContentLoaded', function() {
    
    // Use buttons to switch between Following and For You feeds
    document.querySelector('#ForYou').addEventListener('click', () => Feed_loader('ForYou'));
    document.querySelector('#Following').addEventListener('click', () => Feed_loader('Following'));
    document.querySelector('#compose-btn').addEventListener('click', Compose_post_view);

    // Load Following feed by default
    Feed_loader('Following');
});

function Feed_loader(view) {
    // Toggle visibility for interface elements
    document.querySelector('#homepage').style.display = 'block';
    document.querySelector('#compose-post').style.display = 'none';
    document.querySelector('#compose-btn').style.display = 'block';

    // Clear previous posts
    document.querySelector('#homepage').innerHTML = '';

    // Display loading message
    if (view === 'ForYou') {
        document.querySelector('#homepage').innerHTML = '<p>Loading For You feed...</p>';
        // Call a function or API to load "For You" posts if needed
    } else if (view === 'Following') {
        document.querySelector('#homepage').innerHTML = '<p>Loading Following feed...</p>';
        // Call a function or API to load "Following" posts if needed
    }
}

// Interface behavior for composing a new post
function Compose_post_view(event) {
    event.preventDefault();

    // Toggle visibility for form elements
    document.querySelector('#homepage').style.display = 'none';
    document.querySelector('#compose-post').style.display = 'block';
    document.querySelector('#compose-btn').style.display = 'none';

    // Clear form fields
    const form = document.querySelector('#compose-post-form');
    form.reset();

    // Clear the file input and preview container
    document.querySelector('#upload-images').value = '';
    document.querySelector('#postPreview').innerHTML = '';

    // Remove any previous event listener to prevent duplication and add new listener
    form.removeEventListener('submit', submitFormHandler);
    form.addEventListener('submit', submitFormHandler);
}

async function submitFormHandler(event) {
    event.preventDefault();
    await generate_post();  // Calls the function to post the data
    Feed_loader('Following');  // Return to the Following feed after posting
}
