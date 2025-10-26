from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature
from app.models.user import User
from app.main import main_bp
from flask import current_app
from app.settings.extensions import mail

@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.find_by_email(email)

        if user:
            token = current_app.serializer.dumps(email, salt='password-reset')
            reset_url = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset Request',
                          recipients=[email])
            msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.

This link will expire in 1 hour.
'''
            try:
                mail.send(msg)
                flash('A password reset link has been sent to your email', 'success')
            except Exception as e:
                flash('Error sending email. Please try again later.', 'error')
        else:
            # Don't reveal if email exists or not
            flash('If that email exists, a password reset link has been sent', 'success')

        return redirect(url_for('login'))

    return render_template('forgot_password.html')

@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = current_app.serializer.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired', 'error')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html', token=token)

        if User.update_password(email, password):
            flash('Your password has been reset successfully', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error resetting password', 'error')

    return render_template('reset_password.html', token=token)