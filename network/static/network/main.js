document.addEventListener('DOMContentLoaded', function(){
    // Use buttons to switch between Following and for you

    document.querySelector('#4You').addEventListener('click', ()=> Feed_loader('ForYou'));
    document.querySelector('#Following').addEventListener('click', ()=> Feed_loader('Following'));
    document.querySelector('#compose-post').addEventListener('click', ()=> Compose_post());

    Feed_loader('ForYou');
});

function Feed_loader(view){

    // Hide compose-post and show
    document.querySelector('#homepage').style.display = 'block';
    document.querySelector('#compose-post').style.display = 'none';

    // add line to separate
    document.querySelector('#homepage').innerHTML = `<hr>`;

    // Clear previous posts
    document.querySelector('#homepage').innerHTML += '';



}