function handleFormSubmit(event) {
    event.preventDefault(); // Prevent default form submission
    var ticketId = document.getElementById('ticket_id').value;

    if (ticketId) {
        var url = baseUrl.replace('0', ticketId); // Construct the URL
        window.location.href = url; // Redirect to the constructed URL
    } else {
        alert('Please enter a valid ID.'); // Alert if ticket ID is empty
    }
}
