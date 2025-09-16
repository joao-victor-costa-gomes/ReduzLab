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

// Run the handler once on page load to set the initial state
document.addEventListener('DOMContentLoaded', handleLdaSolverChange);