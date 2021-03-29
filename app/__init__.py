from flask_restplus import Api
from flask import Blueprint

from .main.controller.couriers_controller import api as courier_ns
from .main.controller.orders_controller import api as orders_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title="Candy Delivery App",
    version="1.0",
    description="Service for delivering sweets to sweet teeth"
)

api.add_namespace(courier_ns, path="/couriers")
api.add_namespace(orders_ns, path="/orders")
