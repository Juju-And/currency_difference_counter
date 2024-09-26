from models import Role, db

def create_roles():
    admin = Role(id=1, name='Admin')
    staff = Role(id=3, name='Staff')
    user = Role(id=4, name='User')

    db.session.add(admin)
    db.session.add(user)
    db.session.add(staff)

    db.session.commit()
    print("Roles created successfully!")

create_roles()