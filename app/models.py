from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_value = db.Column(db.Float())
    invoice_currency = db.Column(db.String())
    invoice_issue_date = db.Column(db.String())
    invoice_transfer_date = db.Column(db.String())
    invoice_issue_rate = db.Column(db.Float())
    invoice_transfer_rate = db.Column(db.Float())

    @hybrid_property
    def invoice_value_pln_issue(self):
        return round(self.invoice_value*self.invoice_issue_rate,2)

    @hybrid_property
    def invoice_value_pln_transfer(self):
        return round(self.invoice_value*self.invoice_transfer_rate,2)

    @hybrid_property
    def invoice_exchange_differences(self):
        return round(self.invoice_value_pln_issue-self.invoice_value_pln_transfer,2)

    def __repr__(self):
        return f"Invoice of {self.invoice_issue_date};"

