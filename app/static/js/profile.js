document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        const name = document.getElementById('name').value;
        const bio = document.getElementById('bio').value;
        const location = document.getElementById('location').value;

        if (!name || !bio || !location) {
            event.preventDefault();
            alert('All fields are required.');
        }
    });
});
