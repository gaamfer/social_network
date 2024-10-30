function generate_post(event){
    event.preventDefault();

    const message = document.querySelector('#post-message').value;
    const upload_img = document.querySelector('#upload_images').value;

    fetch('/generate_post', {
        method:'POST',
        body: JSON.stringify({
            message:message,
            images: upload_img
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error){
            // Make an alert with the error
            alert(result.error);
            console.log(result);
            return;
        }
        // Make a alert with the response
        alert(result.message);
        console.log(result);
    });
}