window.addEventListener('load', function() {
        // Check internet connectivity
        fetch('https://www.google.com', {mode: 'no-cors'})
            .then(() => {
                console.log('Internet is available');
            })
            .catch(() => {
                console.log('No internet connection');
                window.location.href = '/no-internet/'; // Redirect to the offline page
            });
    });