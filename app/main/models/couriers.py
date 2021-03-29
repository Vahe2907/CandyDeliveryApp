from sqlalchemy.ext.mutable import MutableList, MutableDict

from .. import db


class Courier(db.Model):
    """" Courier model for storing couriers data """
    __tablename__ = "couriers"

    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.Column(db.String(10))
    regions = db.Column(db.PickleType)
    working_hours = db.Column(db.PickleType)
    average_times = db.Column(MutableDict.as_mutable(db.PickleType))
    current_orders = db.Column(MutableList.as_mutable(db.PickleType))
    orders_complete = db.Column(db.Integer)
    earnings = db.Column(db.Integer)
    checkpoint = db.Column(db.String)
    assign_time = db.Column(db.String)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f"Courier({self.courier_id}, {self.courier_type})"
