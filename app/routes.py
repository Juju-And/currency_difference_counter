from crypt import methods

from flask import render_template, request, redirect, url_for
from models import Invoice, User
from currency import collect_currency_rates
from flask_login import login_user, logout_user, current_user, login_required

def register_routes(app, db, bcrypt):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('welcome'))
            else:
                return "Failed!"

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('welcome'))

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template("signup.html")
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username,password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))


    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('welcome.html')

       # if request.method == 'GET':
       #     invoices = Invoice.query.all()
       #     return render_template("index.html", invoices=invoices)
       # elif request.method == 'POST':
       #     invoice_value = float(request.form.get('invoice_value'))
       #     invoice_issue_date = request.form.get('invoice_issue_date')
       #     invoice_transfer_date = request.form.get('invoice_transfer_date')
       #
       #     date_and_rate = collect_currency_rates(invoice_issue_date, invoice_transfer_date)
       #
       #     invoice = Invoice(invoice_value=invoice_value,
       #                        invoice_issue_date=invoice_issue_date,
       #                        invoice_transfer_date=invoice_transfer_date,
       #                        invoice_issue_rate=date_and_rate["invoice_rate"],
       #                        invoice_transfer_rate=date_and_rate["transfer_rate"]
       #                       )
       #     db.session.add(invoice)
       #     db.session.commit()
       #
       #     invoices = Invoice.query.all()
       #     return render_template("index.html", invoices=invoices)


    # @app.route('/delete/<invoice_id>', methods=['DELETE'])
    # def delete(invoice_id):
    #     Invoice.query.filter(invoice_id == invoice_id).delete()
    #     db.session.commit()
    #
    #     invoices = Invoice.query.all()
    #     return render_template("index.html", invoices=invoices)
    #
    # @app.route('/details/<invoice_id>', methods=['GET'])
    # def details(invoice_id):
    #     invoice = Invoice.query.filter(Invoice.invoice_id == invoice_id).first()
    #     return render_template("details.html", invoice=invoice)