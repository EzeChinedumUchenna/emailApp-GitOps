function sendEmail() {
    var formData = new FormData(document.getElementById('email-form'));
    var sendButton = document.querySelector('.btn-success');

    sendButton.textContent = 'Sending Email...';

    fetch('/send-email', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
            if (data === 'Email sent successfully!') {
                var alertDiv = document.querySelector('#alert');
                alertDiv.className = 'alert alert-success';
                alertDiv.innerHTML = '<p>Email sent successfully!</p>';

                sendButton.textContent = 'Send Email';

                setTimeout(function () {
                    alertDiv.className = '';
                    alertDiv.innerHTML = '';
                }, 5000);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            if (error) {
                var alertDiv = document.querySelector('#alert');
                alertDiv.className = 'alert alert-danger';
                alertDiv.innerHTML = `<p>${error}</p>`;

                sendButton.textContent = 'Send Email';

                setTimeout(function () {
                    alertDiv.className = '';
                    alertDiv.innerHTML = '';
                }, 5000);
            }
        });
}


document.getElementById('email-form').addEventListener('submit', function (event) {
    event.preventDefault();
    sendEmail();
});
