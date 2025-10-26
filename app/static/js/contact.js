document.addEventListener('DOMContentLoaded', function() {
    const addContactForm = document.getElementById('addContactForm');
    const searchContactForm = document.getElementById('searchContactForm');

    if (addContactForm) {
        addContactForm.addEventListener('submit', function(e) {
            const mobilePhone = document.getElementById('mobile_phone').value;
            const email = document.getElementById('email').value;
            const address = document.getElementById('address').value;
            const registrationNumber = document.getElementById('registration_number').value;

            if (!mobilePhone || !email || !address || !registrationNumber) {
                e.preventDefault();
                alert('All fields are required!');
                return false;
            }

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                e.preventDefault();
                alert('Please enter a valid email address!');
                return false;
            }

            const phonePattern = /^[+]?[\d\s-()]+$/;
            if (!phonePattern.test(mobilePhone)) {
                e.preventDefault();
                alert('Please enter a valid phone number!');
                return false;
            }
        });
    }

    if (searchContactForm) {
        searchContactForm.addEventListener('submit', function(e) {
            const registrationNumber = document.getElementById('registration_number').value;

            if (!registrationNumber.trim()) {
                e.preventDefault();
                alert('Please enter a registration number!');
                return false;
            }
        });
    }
});
