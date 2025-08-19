$('#loginForm').on('submit', function(e) {
    e.preventDefault();

    var name = $('#name').val();

    var wherePayload = `this.name == '${name}'`;

    fetch('/gate1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            $where: wherePayload  
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            window.location.href = '/gate2';
        } else {
            $('#failCountMessage').text(data.message);
            alert(data.alert_message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
