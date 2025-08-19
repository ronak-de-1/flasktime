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
            if (data.valid) {
                window.location.href = '/gate1';
            } else {
                alert('Access denied. You are not allowed to proceed.');
            }
        })
        .catch(error => {
            console.error('Error during gate check:', error);
        });
    });
});
