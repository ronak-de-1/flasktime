document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('escapeButton').addEventListener('click', function() {
        // Example payload — you can change this to anything meaningful
        const payload = {
            gateCode: "false", 
        };

        fetch('/gate-check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.result === 'success') {
                window.location.href = '/gate1';
            } else {
                $('#failCountMessage').text(data.message);
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error during gate check:', error);
        });
    });
});
