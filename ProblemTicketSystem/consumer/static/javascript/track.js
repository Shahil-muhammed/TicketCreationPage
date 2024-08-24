// scripts.js
function trackProblem(counter) {
    // Get the input value based on the form's counter
    var inputField = document.getElementById('inputField' + counter);
    var pid = inputField.value;

    // Redirect to the URL with the input value
    if (pid) {
        // Replace the placeholder in the URL with the actual problem ID
        var url = problemUrl.replace('0', pid);
        window.location.href = url;
    } else {
        alert('Please enter a Problem ID.');
    }
}
