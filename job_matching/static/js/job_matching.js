document.addEventListener("DOMContentLoaded", function () {
    const uploadContainer = document.getElementById('uploadContainer');
    const resumeInput = document.getElementById('resumeInput');
    const filePreview = document.getElementById('filePreview');

    // Drag and drop handlers
    ['dragenter', 'dragover'].forEach(event => {
        uploadContainer.addEventListener(event, (e) => {
            e.preventDefault();
            uploadContainer.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(event => {
        uploadContainer.addEventListener(event, (e) => {
            e.preventDefault();
            uploadContainer.classList.remove('dragover');
        });
    });

    uploadContainer.addEventListener('drop', handleDrop);

    resumeInput.addEventListener('change', handleFile);

    function handleFile(e) {
        const file = e.target.files[0];
        updateFilePreview(file);
        uploadContainer.classList.add('d-none');
    }

    function handleDrop(e) {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (!file) return;

        const dt = new DataTransfer();
        dt.items.add(file);
        resumeInput.files = dt.files;

        updateFilePreview(file);
        uploadContainer.classList.add('d-none');
    }

    function updateFilePreview(file) {
        if (file) {
            filePreview.classList.remove('d-none');
            filePreview.querySelector('.file-name').textContent = file.name;
            filePreview.querySelector('.file-size').textContent = (file.size / 1024).toFixed(1) + ' KB';

            const fileIcon = filePreview.querySelector('i');
            fileIcon.className = file.name.endsWith('.pdf')
                ? 'fas fa-file-pdf text-danger me-2'
                : 'fas fa-file-word text-primary me-2';
        }
    }

    window.clearFile = function () {
        resumeInput.value = '';
        filePreview.classList.add('d-none');
        uploadContainer.classList.remove('d-none');
    }
});
