document.getElementById('imageForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    formData.append('image', file);

    try {
        const uploadedImage = document.getElementById('uploadedImage');
        uploadedImage.src = URL.createObjectURL(file);
        document.getElementById('output').style.display = 'block';

        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        console.error(error);
        alert('An error occurred while analyzing the image.');
    }
});

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (result.caption) {
        const caption = document.createElement('p');
        caption.innerHTML = `<strong>Caption:</strong> ${result.caption.text} (Confidence: ${(result.caption.confidence * 100).toFixed(2)}%)`;
        resultsDiv.appendChild(caption);
    }

    if (result.tags) {
        const tags = document.createElement('p');
        tags.innerHTML = `<strong>Tags:</strong> ${result.tags.map(tag => `${tag.name} (${(tag.confidence * 100).toFixed(2)}%)`).join(', ')}`;
        resultsDiv.appendChild(tags);
    }

    if (result.objects) {
        const objects = document.createElement('p');
        objects.innerHTML = `<strong>Objects:</strong> ${result.objects.map(obj => `${obj.tags[0].name} (${(obj.tags[0].confidence * 100).toFixed(2)}%)`).join(', ')}`;
        resultsDiv.appendChild(objects);
    }
}