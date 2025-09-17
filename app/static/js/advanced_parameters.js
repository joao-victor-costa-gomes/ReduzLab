function toggleAdvancedParams() {
    const advancedParamsDiv = document.getElementById('advanced-params');
    if (advancedParamsDiv) {
        advancedParamsDiv.classList.toggle('hidden');
    }
}

function handleLdaSolverChange() {
    const solverSelect = document.getElementById('solver');
    const shrinkageInput = document.getElementById('shrinkage');

    if (!solverSelect || !shrinkageInput) {
        return; // Do nothing if the elements aren't on the page
    }

    // Disable shrinkage input if solver is 'svd'
    if (solverSelect.value === 'svd') {
        shrinkageInput.disabled = true;
        shrinkageInput.value = ''; // Clear the value
        shrinkageInput.placeholder = "Not available for SVD solver";
    } else {
        shrinkageInput.disabled = false;
        shrinkageInput.placeholder = "None, 'auto', or a float 0-1";
    }
}

function handleKpcaKernelChange() {
    const kernelSelect = document.getElementById('kernel');
    if (!kernelSelect) return;

    const selectedKernel = kernelSelect.value;
    
    // Get the containers for the conditional parameters
    const gammaDiv = document.getElementById('kpca_gamma_div');
    const degreeDiv = document.getElementById('kpca_degree_div');
    const coef0Div = document.getElementById('kpca_coef0_div');

    // Show/hide Gamma field
    if (['rbf', 'poly', 'sigmoid'].includes(selectedKernel)) {
        gammaDiv.classList.remove('hidden');
    } else {
        gammaDiv.classList.add('hidden');
    }

    // Show/hide Degree field
    if (selectedKernel === 'poly') {
        degreeDiv.classList.remove('hidden');
    } else {
        degreeDiv.classList.add('hidden');
    }

    // Show/hide Coef0 field
    if (['poly', 'sigmoid'].includes(selectedKernel)) {
        coef0Div.classList.remove('hidden');
    } else {
        coef0Div.classList.add('hidden');
    }
}

// Run the handler once on page load to set the initial state
document.addEventListener('DOMContentLoaded', handleLdaSolverChange);
document.addEventListener('DOMContentLoaded', handleKpcaKernelChange);