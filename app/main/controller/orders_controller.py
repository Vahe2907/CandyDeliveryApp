from flask import request
from flask_restplus import Resource
from ..util.order_dto import OrderDto
from ..services.orders_services import save_new_orders, assign_orders, complete_order

api = OrderDto.api

_order_item = OrderDto.order_item
_orders_post_request = OrderDto.orders_post_request
_orders_assign_post_request = OrderDto.orders_assign_post_request
_orders_complete_post_request = OrderDto.orders_complete_post_request


@api.route("/")
@api.response(201, "Created")
@api.response(400, "Bad request")
class OrdersHandler(Resource):
    @api.doc("Import orders")
    @api.expect(_orders_post_request, validate=True)
    def post(self):
        """ Import couriers """
        data = request.json["data"]
        return save_new_orders(data)


@api.route("/assign")
@api.response(200, "OK")
@api.response(400, "Bad Request")
class OrdersAssign(Resource):
    @api.doc("Assign orders to a courier by id")
    @api.expect(_orders_assign_post_request, validate=True)
    def post(self):
        """ Assign orders to a courier by id """
        data = request.json
        return assign_orders(data)


@api.route("/complete")
@api.response(200, "OK")
@api.response(400, "Bad Request")
class OrdersComplete(Resource):
    @api.doc("Marks orders as completed")
    @api.expect(_orders_complete_post_request, validate=True)
    def post(self):
        """ Marks orders as completed """
        data = request.json
        return complete_order(data)
