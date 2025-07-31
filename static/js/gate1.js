$('#loginForm').on('submit', function(e) {
    e.preventDefault();

    var username = $('#username').val();

    // Create a JS expression string for $where injection
    var wherePayload = `this.username == '${username}'`;

    fetch('/gate1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            $where: wherePayload  // Send raw JS expression for backend $where query
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            window.location.href = '/gate2';
        } else {
            failmessage = data.result + " " +data.failcount
            alert(failmessage);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
