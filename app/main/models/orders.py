from .. import db


class Order(db.Model):
    """" Order model for storing orders data """
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    region = db.Column(db.Integer)
    delivery_hours = db.Column(db.PickleType)
    available = db.Column(db.Boolean)
    courier_id = db.Column(db.Integer)

    def __repr__(self):
        return f"Order({self.order_id}, {self.weight})"
