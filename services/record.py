from datetime import datetime

from database.models import Record


def add_record(session, user_id, dialogue_id):
    new_record = Record(
        Id=user_id,
        D_id=dialogue_id,
        R_time=datetime.now()  # 自动设置记录时间为当前时间
    )
    session.add(new_record)
    session.commit()
def get_record(session, user_id, dialogue_id):
    return session.query(Record).filter(Record.Id == user_id, Record.D_id == dialogue_id).first()
def update_record_time(session, record):
    record.R_time = datetime.now()
    session.commit()
def delete_record(session, user_id, dialogue_id):
    record = session.query(Record).filter(Record.Id == user_id, Record.D_id == dialogue_id).first()
    if record:
        session.delete(record)
        session.commit()
def get_records_by_user(session, user_id):
    return session.query(Record).filter(Record.Id == user_id).all()
def get_records_by_dialogue(session, dialogue_id):
    return session.query(Record).filter(Record.D_id == dialogue_id).all()
