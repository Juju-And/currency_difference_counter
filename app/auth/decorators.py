from functools import wraps
from flask import redirect, flash, url_for
from flask_login import login_required, current_user


# Custom decorator to check for admin role
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
