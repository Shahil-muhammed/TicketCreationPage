console.log('problemUrl:', problemUrl);

function issue(counter) {
    // Get the input value based on the form's counter
    var inputField = document.getElementById('inputField' + counter);
    if (inputField) {
        var pid = inputField.value;

        // Redirect to the URL with the input value
        if (pid) {
            // Create the correct URL with the input value
            var url = problemUrl.replace('0', pid);
            console.log('Redirecting to:', url); // Debugging
            window.location.href = url;
        } else {
            alert('Please enter a Problem ID.');
        }
    } else {
        console.error('Input field with ID inputField' + counter + ' not found');
    }
}
