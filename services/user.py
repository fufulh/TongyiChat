from database.models import User


def add_user(session, user_id, name, password, registration_date, last_login_time):
    new_user = User(
        Id=user_id,
        Name=name,
        Password=password,
        Registration_date=registration_date,
        Last_login_time=last_login_time
    )
    session.add(new_user)
    session.commit()
def get_user_by_id(session, user_id):
    return session.query(User).filter(User.Id == user_id).first()
def update_user(session, user):
    session.commit()
def delete_user(session, user_id):
    user = session.query(User).filter(User.Id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
def verify_password(session, user_id, password):
    user = get_user_by_id(session, user_id)
    return user and user.Password == password
import datetime

def update_last_login(session, user_id):
    user = get_user_by_id(session, user_id)
    if user:
        user.Last_login_time = datetime.datetime.now()
        session.commit()
