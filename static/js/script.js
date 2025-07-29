document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('logForm');
    const submitButton = form.querySelector('.primary-button');
    const buttonText = submitButton.querySelector('.button-text');
    const spinner = submitButton.querySelector('.spinner');
    const resultsSection = document.getElementById('results');
    const errorSection = document.getElementById('error');
    const fileInput = document.getElementById('log_file');
    const textInput = document.getElementById('log_text');

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        setLoadingState(true);
        
        // Hide previous results/errors
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        
        // Prepare form data
        const formData = new FormData();
        
        // Add file if selected
        if (fileInput.files.length > 0) {
            formData.append('log_file', fileInput.files[0]);
        }
        
        // Add text content
        formData.append('log_text', textInput.value);
        
        // Add options
        formData.append('include_spans', document.getElementById('include_spans').checked ? 'true' : 'false');
        formData.append('verbose', document.getElementById('verbose').checked ? 'true' : 'false');
        
        // Submit to server
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            setLoadingState(false);
            
            if (data.success) {
                showResults(data);
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            setLoadingState(false);
            showError('Network error: ' + error.message);
        });
    });

    // File input change handler
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            // Clear text input when file is selected
            textInput.value = '';
            
            // Optional: Show file name
            console.log('File selected:', this.files[0].name);
        }
    });

    // Text input change handler
    textInput.addEventListener('input', function() {
        if (this.value.trim()) {
            // Clear file input when text is entered
            fileInput.value = '';
        }
    });

    // Copy button functionality
    document.addEventListener('click', function(e) {
        if (e.target.id === 'copyButton') {
            copyToClipboard();
        } else if (e.target.id === 'downloadButton') {
            downloadQuery();
        }
    });

    function setLoadingState(loading) {
        if (loading) {
            submitButton.disabled = true;
            submitButton.classList.add('loading');
            buttonText.style.opacity = '0';
            spinner.style.display = 'block';
        } else {
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
            buttonText.style.opacity = '1';
            spinner.style.display = 'none';
        }
    }

    function showResults(data) {
        const resultInfo = document.getElementById('result-info');
        const dqlOutput = document.getElementById('dql-output');
        
        resultInfo.textContent = `Found ${data.count} ${data.count_type}`;
        dqlOutput.textContent = data.dql_query;
        
        // Store query for download
        window.currentQuery = data.dql_query;
        
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function showError(message) {
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Scroll to error
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function copyToClipboard() {
        const dqlOutput = document.getElementById('dql-output');
        const text = dqlOutput.textContent;
        
        if (navigator.clipboard && window.isSecureContext) {
            // Use modern clipboard API
            navigator.clipboard.writeText(text).then(function() {
                showCopyFeedback('Copied to clipboard!');
            }).catch(function(err) {
                console.error('Failed to copy: ', err);
                fallbackCopyTextToClipboard(text);
            });
        } else {
            // Fallback for older browsers
            fallbackCopyTextToClipboard(text);
        }
    }

    function fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        
        // Avoid scrolling to bottom
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.position = "fixed";
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                showCopyFeedback('Copied to clipboard!');
            } else {
                showCopyFeedback('Copy failed. Please select and copy manually.', true);
            }
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
            showCopyFeedback('Copy failed. Please select and copy manually.', true);
        }
        
        document.body.removeChild(textArea);
    }

    function showCopyFeedback(message, isError = false) {
        const copyButton = document.getElementById('copyButton');
        const originalText = copyButton.textContent;
        
        copyButton.textContent = message;
        copyButton.style.background = isError ? '#fed7d7' : '#c6f6d5';
        copyButton.style.color = isError ? '#c53030' : '#276749';
        
        setTimeout(() => {
            copyButton.textContent = originalText;
            copyButton.style.background = '';
            copyButton.style.color = '';
        }, 2000);
    }

    function downloadQuery() {
        if (!window.currentQuery) {
            showCopyFeedback('No query to download', true);
            return;
        }
        
        // Create download URL
        const queryParam = encodeURIComponent(window.currentQuery);
        const downloadUrl = `/download?query=${queryParam}`;
        
        // Create temporary link and click it
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = 'trace_query.dql';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Show feedback
        const downloadButton = document.getElementById('downloadButton');
        const originalText = downloadButton.textContent;
        downloadButton.textContent = '✅ Downloaded!';
        setTimeout(() => {
            downloadButton.textContent = originalText;
        }, 2000);
    }

    // Add example data functionality
    function loadExampleData() {
        const exampleLog = `2025-07-26 16:34:50.031 INFO  XxxxAdapter.lambda$afterBodyRead$0(): [http-nio-8080-exec-5] [T-a9f624ee2e4f3c9b,S-a9f624ee2e4f3c9b] :   [POST] /xxx/xx/xxxx
2025-07-26 16:34:50.060 INFO  XxxxAdapter.lambda$afterBodyRead$0(): [http-nio-8080-exec-4] [T-f0c8e2a82b6a2349,S-f0c8e2a82b6a2349] :   [POST] /xxx/xx/xxxx
2025-07-26 16:34:51.123 INFO  XxxxAdapter.lambda$afterBodyRead$0(): [http-nio-8080-exec-6] [T-01ca3088195366d4,S-01ca3088195366d4] :   [POST] /xxx/xx/xxxx`;
        
        textInput.value = exampleLog;
        fileInput.value = '';
    }

    // Add example button (you can add this to HTML if desired)
    window.loadExampleData = loadExampleData;
});