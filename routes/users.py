from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Branch, Sale
from extensions import db, bcrypt
from decorators import admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
@admin_required
def index(): #(def in phyton is a function  index gina show ya ang tanan nga list of users,)
    users = User.query.all()
    return render_template('users/index.html', users=users)

@users_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    branches = Branch.query.all()
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        branch_id = request.form.get('branch_id')
        role = request.form.get('role', 'staff')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('users.add'))
        if email and User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('users.add'))
            
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            branch_id=branch_id if branch_id else None,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {username} created successfully!', 'success')
        return redirect(url_for('users.index'))
        
    return render_template('users/create.html', branches=branches)

@users_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(user_id):
    user = User.query.get_or_404(user_id)
    branches = Branch.query.all()
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        branch_id = request.form.get('branch_id')
        user.branch_id = branch_id if branch_id else None
        user.role = request.form.get('role')
        
        password = request.form.get('password')
        if password:
            user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
        db.session.commit()
        flash(f'User {user.username} updated successfully!', 'success')
        return redirect(url_for('users.index'))
        
    return render_template('users/edit.html', user=user, branches=branches)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('users.index'))
    
    # Check for dependencies (Sales)
    has_sales = Sale.query.filter_by(user_id=user.id).first()
    if has_sales:
        flash('Cannot delete user with existing sales history. Reassign sales or deactivate instead.', 'danger')
        return redirect(url_for('users.index'))
        
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('users.index'))
