import generate_post from "./network/static/network/api.js";

document.addEventListener('DOMContentLoaded', function(){
    
    // Use buttons to switch between Following and for you

    document.querySelector('#ForYou').addEventListener('click', () => Feed_loader('ForYou'));
    document.querySelector('#Following').addEventListener('click', () => Feed_loader('Following'));
    document.querySelector('#compose-btn').addEventListener('click', Compose_post_view);

    Feed_loader('Following');

});

function Feed_loader(view){
    // JUSt THE BEHAVIOUR 

    // Hide compose-post and show
    document.querySelector('#homepage').style.display = 'block';
    document.querySelector('#compose-post').style.display = 'none';
    document.querySelector('#compose-btn').style.display = 'block';
    
    // Clear previous posts
    document.querySelector('#homepage').innerHTML = '';

    // Load the appropriate feed based on the view
    if (view === 'ForYou') {
        document.querySelector('#homepage').innerHTML = '<p>Loading For You feed...</p>';
    } else if (view === 'Following') {
        document.querySelector('#homepage').innerHTML = '<p>Loading Following feed...</p>';
    }
};


// This s just for the Interface behaviour
function Compose_post_view(){
    // Just adjust the behaviour of the form showing up 
    document.querySelector('#homepage').style.display='none';
    document.querySelector('#compose-post').style.display='block';
    document.querySelector('#compose-btn').style.display='none';

    
    document.querySelector('#compose-post-form').addEventListener('submit', generate_post);
    
};


