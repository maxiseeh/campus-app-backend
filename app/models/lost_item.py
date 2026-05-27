from datetime import datetime
from ..extensions import db


class LostItem(db.Model):
    __tablename__ = "lost_items"

    id = db.Column(db.BigInteger, primary_key=True)
    item_name = db.Column(db.Text)
    description = db.Column(db.Text)
    status = db.Column(db.Text)
    image_url = db.Column(db.Text)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
