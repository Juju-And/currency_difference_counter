from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True)
    _password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return f"User: {self.username}, Role: {self.role}"

    def get_id(self):
        return self.uid

    roles = db.relationship("Role", secondary="user_roles", back_populates="users")

    def has_role(self, role):
        return bool(
            Role.query
            .join(Role.users)
            .filter(User.id == self.uid)
            .filter(Role.slug == role)
            .count() == 1
        )

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(36), nullable=False)
    slug = db.Column(db.String(36), nullable=False, unique=True)
    users = db.relationship("User", secondary="user_roles", back_populates="roles")

class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_value = db.Column(db.Float())
    invoice_currency = db.Column(db.String())
    invoice_issue_date = db.Column(db.String())
    invoice_transfer_date = db.Column(db.String())
    invoice_issue_rate = db.Column(db.Float())
    invoice_transfer_rate = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey(User.uid))

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
        return f"Invoice of {self.invoice_issue_date}"

