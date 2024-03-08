changePasswordForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const currentPassword = this.querySelector('#currentPassword').value;
    const newPassword = this.querySelector('#newPassword').value;
  
    fetch('/dashboard/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'currentPassword': currentPassword,
        'newPassword': newPassword
      })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
  });
  