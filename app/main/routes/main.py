from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.models.contact import Contact
from flask_login import login_required
from app.main import main_bp
@main_bp.route('/')
def index():
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    contacts = Contact.find_all_by_user(current_user.id)
    return render_template('dashboard.html', contacts=contacts)

@main_bp.route('/add-contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        mobile_phone = request.form.get('mobile_phone')
        email = request.form.get('email')
        address = request.form.get('address')
        registration_number = request.form.get('registration_number')

        if not all([mobile_phone, email, address, registration_number]):
            flash('All fields are required', 'error')
            return render_template('add_contact.html')

        contact_id = Contact.create_contact(
            current_user.id,
            mobile_phone,
            email,
            address,
            registration_number
        )

        if contact_id:
            flash('Contact added successfully', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Registration number already exists', 'error')

    return render_template('add_contact.html')

@main_bp.route('/search-contact', methods=['GET', 'POST'])
@login_required
def search_contact():
    contact = None
    if request.method == 'POST':
        registration_number = request.form.get('registration_number')
        contact = Contact.find_by_registration_number(registration_number)

        if not contact:
            flash('No contact found with that registration number', 'error')

    return render_template('search_contact.html', contact=contact)


