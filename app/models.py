from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return f"User: {self.username}, Role: {self.role}"

    def get_id(self):
        return self.uid


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

