export function generate_post(event){
    event.preventDefault();

    const message = document.querySelector('#post-message').value;
    const upload_img = document.querySelector('#upload_images').files;
    
    const formData = new FormData();

    formData.append('message', message);
    // Append each image individually 
    for (let i=0 ; i < upload_img.length; i++) {
        formData.append('images', upload_img[i]);
    }

    fetch('/generate_post', {
        method:'POST',
        body: formData
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