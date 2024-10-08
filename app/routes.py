from datetime import datetime
from secrets import token_urlsafe

from flask import render_template, request, redirect, url_for, session, flash

from app import mail
from auth.decorators import admin_required
from models import Invoice, User
from currency import collect_currency_rates
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def register_routes(app, db, bcrypt):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user._password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return "Failed!"

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template("signup.html")
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
            token = token_urlsafe(16)

            user = User(username=username,_password=hashed_password,email=email,created_on=datetime.now())

            db.session.add(user)
            db.session.commit()
            msg = Message(subject='Please verify your account', sender='currency_converter@mailtrap.io',
                          recipients=[email])
            msg.body = (f"Here is your token"
                        f"\nhttp://127.0.0.1:5000/user/activate/{token}")
            mail.send(msg)


            return redirect(url_for('login'))

    @app.route("/send_mail")
    def sending_mail():
        msg = Message(subject='Hello from the other side!', sender='peter@mailtrap.io', recipients=['kezxqacjppolequuao@hthlm.com'])
        msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works trololo"
        mail.send(msg)
        return "Message sent!"


        # mail_message = Message(
        #     subject='Hi ! Don’t forget to follow me for more article!',
        #     recipients=['kezxqacjppolequuao@hthlm.com'])
        # mail_message.body = "This is a test"
        # mail.send(mail_message)
        # return "Mail has sent"


    @app.route('/user/activate/<token>', methods=['GET', 'POST'])
    def confirm_email(token):
        # if current_user.confirmed_on is not None:
        #     flash("Account already confirmed.", "success")
        #     return redirect(url_for("core.home"))
        current_user.confirmed_on = datetime.now()




    @app.route('/', methods=['GET', 'POST'])
    def index():
       if not current_user.is_authenticated:
            return render_template('welcome.html')

       if request.method == 'POST':
           invoice_value = float(request.form.get('invoice_value'))
           invoice_issue_date = request.form.get('invoice_issue_date')
           invoice_transfer_date = request.form.get('invoice_transfer_date')

           date_and_rate = collect_currency_rates(invoice_issue_date, invoice_transfer_date)

           invoice = Invoice(invoice_value=invoice_value,
                              invoice_issue_date=invoice_issue_date,
                              invoice_transfer_date=invoice_transfer_date,
                              invoice_issue_rate=date_and_rate["invoice_rate"],
                              invoice_transfer_rate=date_and_rate["transfer_rate"],
                              user_id=current_user.uid
                             )
           db.session.add(invoice)
           db.session.commit()

       invoices = Invoice.query.filter(Invoice.user_id == current_user.uid).all()
       return render_template("index.html", invoices=invoices)


    @app.route('/delete/<invoice_id>', methods=['DELETE'])
    @login_required
    def delete(invoice_id):
        Invoice.query.filter(invoice_id == invoice_id).delete()
        db.session.commit()

        invoices = Invoice.query.all()
        return render_template("index.html", invoices=invoices)

    @app.route('/details/<invoice_id>', methods=['GET'])
    @login_required
    def details(invoice_id):
        invoice = Invoice.query.filter(Invoice.invoice_id == invoice_id).first()
        return render_template("details.html", invoice=invoice)



    @app.route('/admin_dashboard')  # @route() must always be the outer-most decorator
    @admin_required
    def admin_dashboard():
        users = User.query.all()
        return render_template("admin.html", users=users)