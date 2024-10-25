document.addEventListener('DOMContentLoaded', function(){
    
    // Use buttons to switch between Following and for you

    document.querySelector('#ForYou').addEventListener('click', () => Feed_loader('ForYou'));
    document.querySelector('#Following').addEventListener('click', () => Feed_loader('Following'));
    document.querySelector('#compose-btn').addEventListener('click', () => Compose_post());
    document.querySelector('#Following').addEventListener('click', () => Followers());

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

    // add line to separate
    document.querySelector('#homepage').innerHTML = `<hr>`;


    // Load the appropriate feed based on the view
    if (view === 'ForYou') {
        document.querySelector('#homepage').innerHTML += '<p>Loading For You feed...</p>';
    } else if (view === 'Following') {
        document.querySelector('#homepage').innerHTML += '<p>Loading Following feed...</p>';
    }
}


// THIs s just for the Interface behaviour
function Compose_post(){
    // Just adjust the behaviour of the form showing up 

    document.querySelector('#homepage').style.display='none';
    document.querySelector('#compose-post').style.display='block';
    document.querySelector('#compose-btn').style.display='none';

    
}

function Search(){
    
    // Hide search-area-button
    document.querySelector('#search-area-button').style.display = 'none';
    document.querySelector('#search-area').style.display = 'block';

    // When press the left arrow go back
    document.querySelector('#search-area-left').addEventListener('click', () => HideSearchArea());

};
