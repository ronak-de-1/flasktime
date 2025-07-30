$('#loginForm').on('submit', function(e) {
    e.preventDefault();

    var username = $('#username').val();
    var password = $('#password').val();

    // Create a JS expression string for $where injection
    var wherePayload = `this.username == '${username}' && this.password == '${password}'`;

    fetch('/gate2', {
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
            window.location.href = '/login';
        } else {
            alert("hello",data.result);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
