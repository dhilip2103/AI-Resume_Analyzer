        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('resumeFile');
        const fileName = document.getElementById('fileName');
        const errorAlert = document.getElementById('errorAlert');
        const submitBtn = document.querySelector('.submit-text');
        const spinner = document.getElementById('spinner');
        const filePreview = document.getElementById('filePreview');
        const previewFileName = document.getElementById('previewFileName');
        const fileIcon = filePreview.querySelector('.file-icon');

        // Drag & Drop handlers
        dropZone.addEventListener('click', () => fileInput.click());
        
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length) {
                handleFile(files[0]);
            }
        });

        // File input change handler
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFile(e.target.files[0]);
            }
        });

        // Form submission handler
        document.getElementById('uploadForm').addEventListener('submit', (e) => {
            if (!fileInput.files.length) {
                e.preventDefault();
                showError('Please select a file first!');
            } else {
                submitBtn.textContent = 'Analyzing...';
                spinner.classList.remove('d-none');
            }
        });

        function handleFile(file) {
            const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            
            if (!validTypes.includes(file.type)) {
                showError('Invalid file type. Please upload a PDF or DOCX file.');
                fileInput.value = '';
                return;
            }

            // Update UI
            fileName.textContent = file.name;
            dropZone.classList.add('d-none');
            filePreview.classList.remove('d-none');
            previewFileName.textContent = file.name;

            // Set appropriate icon
            if (file.type === 'application/pdf') {
                fileIcon.className = 'file-icon text-danger fas fa-file-pdf';
            } else {
                fileIcon.className = 'file-icon text-primary fas fa-file-word';
            }

            errorAlert.classList.add('d-none');
        }

        function showError(message) {
            errorAlert.textContent = message;
            errorAlert.classList.remove('d-none');
            setTimeout(() => errorAlert.classList.add('d-none'), 5000);
            
            // Reset UI on error
            dropZone.classList.remove('d-none');
            filePreview.classList.add('d-none');
            fileName.textContent = 'No file selected';
            fileInput.value = '';
        }