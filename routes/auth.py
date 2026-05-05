from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, OTP, PasswordReset, Branch
from extensions import db, bcrypt, mail
from flask_mail import Message
import random
import uuid
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        identity = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter((User.username == identity) | (User.email == identity)).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not user.email:
                flash('No email associated with this account. Please contact admin.', 'danger')
                return redirect(url_for('auth.login'))
            
            # 1. Generate OTP
            otp_code = '{:06d}'.format(random.randint(0, 999999))
            otp = OTP(user_id=user.id, otp_code=otp_code, expires_at=datetime.utcnow() + timedelta(minutes=15))
            try:
                # 2. Save to DB first
                db.session.add(otp)
                db.session.commit()
                
                # 3. Attempt to send Email
                msg = Message('Your H2Ops Login OTP', recipients=[user.email])
                msg.body = f"Your OTP for login is: {otp_code}\n\nIt will expire in 5 minutes."
                mail.send(msg)
                
                session['pending_user_id'] = user.id
                flash('OTP sent to your email.', 'info')
                return redirect(url_for('auth.verify_otp'))
                
            except Exception as e:
                db.session.rollback() # Rollback if DB or Mail fails
                print(f"CRITICAL LOGIN ERROR: {e}")
                
                # This prevents the "Internal Server Error" white screen
                flash(f'System Error: Could not send OTP. (Error: {str(e)})', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html')


@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'pending_user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        otp_code = request.form.get('otp_code')
        user_id = session.get('pending_user_id')
        
        valid_otp = OTP.query.filter_by(user_id=user_id, otp_code=otp_code, is_used=False).filter(OTP.expires_at > datetime.utcnow()).first()
        
        if valid_otp:
            valid_otp.is_used = True
            db.session.commit()
            
            user = User.query.get(user_id)
            login_user(user)
            # Set active branch for the session
            session['active_branch_id'] = user.branch_id
            session.pop('pending_user_id', None)
            flash('Login successful.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid or expired OTP.', 'danger')
            
    return render_template('verify_otp.html')

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = str(uuid.uuid4())
            reset = PasswordReset(user_id=user.id, reset_token=token, expires_at=datetime.utcnow() + timedelta(minutes=15))
            db.session.add(reset)
            db.session.commit()
            
            # Send Email
            try:
                msg = Message('H2Ops Password Reset', recipients=[user.email])
                reset_link = url_for('auth.reset_password', token=token, _external=True)
                msg.body = f"To reset your password, click the following link:\n{reset_link}\n\nThis link expires in 15 minutes."
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'info')
            except Exception as e:
                flash('Failed to send reset email. Check terminal for error.', 'danger')
                print(f"Mail sending error: {e}")
        else:
            flash('If an account with that email exists, a reset link was sent.', 'info')

        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset = PasswordReset.query.filter_by(reset_token=token, is_used=False).filter(PasswordReset.expires_at > datetime.utcnow()).first()
    
    if not reset:
        flash('Invalid or expired reset token.', 'danger')
        return redirect(url_for('auth.forgot_password'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html', token=token)
            
        user = User.query.get(reset.user_id)
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        reset.is_used = True
        db.session.commit()
        
        flash('Password successfully reset. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('reset_password.html', token=token)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('pending_user_id', None)
    session.pop('active_branch_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/switch_branch/<int:branch_id>')
@login_required
def switch_branch(branch_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    if branch_id == 0:
        session.pop('active_branch_id', None)
        flash("Switched to Global Overview", "info")
        return redirect(request.referrer or url_for('main.dashboard'))
        
    branch = Branch.query.get_or_404(branch_id)
    session['active_branch_id'] = branch.id
    flash(f"Switched to {branch.name}", "info")
    return redirect(request.referrer or url_for('main.dashboard'))
