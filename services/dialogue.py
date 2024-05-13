from database.models import Dialogue


def add_dialogue(session, d_id, dialogue_type, content):
    new_dialogue = Dialogue(
        D_id=d_id,
        Type=dialogue_type,
        Content=content
    )
    session.add(new_dialogue)
    session.commit()
def get_dialogue_by_id(session, d_id):
    return session.query(Dialogue).filter(Dialogue.D_id == d_id).first()
def update_dialogue(session, dialogue):
    session.commit()
def delete_dialogue(session, d_id):
    dialogue = session.query(Dialogue).filter(Dialogue.D_id == d_id).first()
    if dialogue:
        session.delete(dialogue)
        session.commit()
def get_dialogues_by_type(session, dialogue_type):
    return session.query(Dialogue).filter(Dialogue.Type == dialogue_type).all()
