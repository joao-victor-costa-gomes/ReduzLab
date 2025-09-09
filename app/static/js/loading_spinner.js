function showLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    const runButton = document.getElementById('run-button');

    if (spinner) {
        spinner.classList.remove('hidden');
    }

    if (runButton) {
        runButton.disabled = true;
        runButton.innerText = 'Processing...';
    }
}