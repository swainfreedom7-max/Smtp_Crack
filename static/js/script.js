// Theme Toggle
const themeToggle = document.querySelector('.theme-toggle');
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    document.body.classList.toggle('dark-mode');
    document.body.setAttribute('data-theme', 
        document.body.classList.contains('dark-mode') ? 'dark' : 'light'
    );
    
    localStorage.setItem('theme', 
        document.body.classList.contains('dark-mode') ? 'dark' : 'light'
    );
    
    const icon = themeToggle.querySelector('i');
    icon.classList.toggle('fa-moon');
    icon.classList.toggle('fa-sun');
});

// Check for saved theme preference
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode');
    document.body.setAttribute('data-theme', 'dark');
    const icon = themeToggle.querySelector('i');
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
}

// File Drag and Drop
const fileDropZone = document.getElementById('fileDropZone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');

fileDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileDropZone.classList.add('dragover');
});

fileDropZone.addEventListener('dragleave', () => {
    fileDropZone.classList.remove('dragover');
});

fileDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    fileDropZone.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        updateFilePreview(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        updateFilePreview(e.target.files[0]);
    }
});

function updateFilePreview(file) {
    if (file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        filePreview.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file-alt"></i>
                <div>
                    <strong>${file.name}</strong>
                    <span>${fileSize} MB</span>
                </div>
            </div>
        `;
        filePreview.classList.add('active');
    }
}

// Loading Animation
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('active');
    
    const progressBar = document.getElementById('progressBar');
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 10;
        progressBar.style.width = `${Math.min(progress, 100)}%`;
        if (progress >= 100) clearInterval(interval);
    }, 300);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('active');
    document.getElementById('progressBar').style.width = '0%';
}

// Form submission
document.querySelector('.upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!fileInput.files.length) {
        showNotification('Please select a file first!', 'error');
        return;
    }
    
    showLoading();
    
    // Simulate processing
    setTimeout(() => {
        this.submit();
    }, 2000);
});

// Notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}