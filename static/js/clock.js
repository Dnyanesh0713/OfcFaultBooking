       function updateDateTime() {
        const now = new Date();

        // Get day name, month name, day, and year
        const options = { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' };
        const dateString = now.toLocaleDateString('en-US', options);

        // Format time
        let hours = now.getHours();
        let minutes = now.getMinutes().toString().padStart(2, '0');
        let seconds = now.getSeconds().toString().padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12 || 12; // Convert to 12-hour format
        const timeString = `${hours}:${minutes}:${seconds} ${ampm}`;

        // Display date and time
        document.getElementById("date-time").textContent = `${dateString} :: ${timeString}`;
    }

    // Update date and time immediately and then every second
    updateDateTime();
    setInterval(updateDateTime, 1000);
