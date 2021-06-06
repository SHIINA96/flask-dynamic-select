from app import SQLAlchemy, db, datetime
 
class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(140), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(140), nullable=False)
    size = db.Column(db.Integer, nullable=True)
    prize = db.Column(db.Float, nullable=True)
    shipment = db.Column(db.Float, nullable=True)
    totalPrize = db.Column(db.Float, nullable=True)
    consumable = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(140), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False) # class 名字小写识别为 User 表
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)