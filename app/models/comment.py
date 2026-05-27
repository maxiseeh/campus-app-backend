from datetime import datetime
from ..extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    post_id = db.Column(db.BigInteger, db.ForeignKey("posts.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
