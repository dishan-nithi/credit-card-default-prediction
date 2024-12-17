document.getElementById("uploadForm").addEventListener('submit', function(event) {
    event.preventDefault();

    document.getElementById('fileError').textContent = '';

    const fileInput = document.getElementById('attachment');
    const file = fileInput.files[0]; // Corrected to `files`

    if (!file) {
        document.getElementById('fileError').textContent = 'Please select a CSV file to upload.';
        return;
    }

    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (fileExtension !== 'csv') {
        document.getElementById('fileError').textContent = `Only CSV files are allowed. ${fileExtension}`;
        return;
    }

    document.getElementById('resultMessage').style.display = 'block';
    document.getElementById('resultText').textContent = `Your file '${file.name}' has been successfully uploaded.`;
});
