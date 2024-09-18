from flask import render_template, request
from models import Invoice
from currency import collect_currency_rates

def register_routes(app, db):
    @app.route('/', methods=['GET', 'POST'])
    def index():
       if request.method == 'GET':
           invoices = Invoice.query.all()
           return render_template("index.html", invoices=invoices)
       elif request.method == 'POST':
           invoice_value = float(request.form.get('invoice_value'))
           invoice_issue_date = request.form.get('invoice_issue_date')
           invoice_transfer_date = request.form.get('invoice_transfer_date')

           date_and_rate = collect_currency_rates(invoice_issue_date, invoice_transfer_date)

           invoice = Invoice(invoice_value=invoice_value,
                              invoice_issue_date=invoice_issue_date,
                              invoice_transfer_date=invoice_transfer_date,
                              invoice_issue_rate=date_and_rate["invoice_rate"],
                              invoice_transfer_rate=date_and_rate["transfer_rate"]
                             )
           db.session.add(invoice)
           db.session.commit()

           invoices = Invoice.query.all()
           return render_template("index.html", invoices=invoices)


    @app.route('/delete/<invoice_id>', methods=['DELETE'])
    def delete(invoice_id):
        Invoice.query.filter(invoice_id == invoice_id).delete()
        db.session.commit()

        invoices = Invoice.query.all()
        return render_template("index.html", invoices=invoices)

    @app.route('/details/<invoice_id>', methods=['GET'])
    def details(invoice_id):
        invoice = Invoice.query.filter(Invoice.invoice_id == invoice_id).first()
        return render_template("details.html", invoice=invoice)