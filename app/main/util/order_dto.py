from flask_restplus import Namespace, fields


class OrderDto:
    api = Namespace("orders", description="orders related requests")

    order_item = api.model("OrderItem", {
        "order_id": fields.Integer(required=True, description="order unique ID"),
        "weight": fields.Fixed(decimals=2, required=True, description="order weight"),
        "region": fields.Integer(requiered=True, description="order region"),
        "delivery_hours": fields.List(fields.String, required=True, description="order delivery hours")
    })

    orders_post_request = api.model("OrderPostRequest", {
        "data": fields.List(fields.Nested(order_item), required=True, description="list of orders")
    })

    orders_assign_post_request = api.model("OrdersAssignPostRequest", {
        "courier_id": fields.Integer(required=True, description="courier ID"),
    })

    orders_complete_post_request = api.model("OrdersCompletePostRequest", {
        "courier_id": fields.Integer(required=True, description="courier ID"),
        "order_id": fields.Integer(required=True, description="order ID"),
        "complete_time": fields.String(required=True, description="complete time")
    })
