from datetime import datetime
from ..extensions import db


class StudyGroup(db.Model):
    __tablename__ = "study_groups"

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    tech_stack = db.Column(db.Text)
    meeting_time = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
