export async function generate_post() {
    const message = document.querySelector('#post-message').value;
    const uploadImg = document.querySelector('#upload-images').files;

    // Validate form data (optional: customize validation as needed)
    if (!message.trim() && uploadImg.length === 0) {
        alert("Please enter a message or upload at least one image.");
        return;
    }

    const formData = new FormData();
    formData.append('message', message);

    // Append each image individually
    for (let i = 0; i < uploadImg.length; i++) {
        formData.append('images', uploadImg[i]);
    }

    try {
        const response = await fetch('/generate_post', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();

        if (result.error) {
            alert(result.error);
            console.error("Error from server:", result);
            return;
        }

        alert(result.message);
        console.log("Post created successfully:", result);

    } catch (error) {
        console.error('Network or server error:', error);
        alert("An error occurred while creating the post. Please try again.");
    }
}
