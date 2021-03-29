from flask_restplus import marshal

from app.main import db
from app.main.models.couriers import Courier
from app.main.models.orders import Order

from ..util.handlers import parse_interval, compatible, hours_intersection_check
from ..util.courier_dto import CourierDto

_courier_item = CourierDto.courier_item
_courier_get_response_with_rating = CourierDto.courier_get_response_with_rating
_courier_get_response = CourierDto.courier_get_response
_courier_update_request = CourierDto.courier_update_request


def save_new_courier(data):
    courier = Courier.query.filter_by(courier_id=data["courier_id"]).first()

    if courier:
        return data["courier_id"], 1

    new_courier = Courier(
        courier_id=data["courier_id"],
        courier_type=data["courier_type"],
        regions=data["regions"],
        working_hours=data["working_hours"],
        average_times={},
        current_orders=[],
        orders_complete=0,
        earnings=0,
        checkpoint=None,
        assign_time=None
    )

    for interval in new_courier.working_hours:
        res = parse_interval(interval)
        if res["status"]:
            return new_courier.courier_id, 1

    save_changes(new_courier)

    return data["courier_id"], 0


def save_new_couriers(data):
    succeed_ids = []
    fail_ids = []

    for micro_data in data:
        courier_id, state = save_new_courier(micro_data)
        if state:
            fail_ids.append({"id": courier_id})
        else:
            succeed_ids.append({"id": courier_id})

    if fail_ids:
        response_object = {
            "validation_error": {
                "couriers": fail_ids
            }
        }

        return response_object, 400

    response_object = {
        "couriers": succeed_ids
    }

    return response_object, 201


def get_courier(courier_id):
    courier = Courier.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return None, 404

    if not courier.orders_complete:
        return marshal(courier, _courier_get_response), 200

    t = min([sum(courier.average_times[rg]) / len(courier.average_times[rg]) for rg in courier.average_times])
    courier.rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5

    return marshal(courier, _courier_get_response_with_rating), 200


def update_courier(courier_id, data):
    courier = Courier.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return None, 404

    for field in data:
        if field not in _courier_update_request:
            return None, 400

        setattr(courier, field, data[field])

    new_orders = []
    for order_id in courier.current_orders:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            continue

        if (not compatible(order.weight, courier.courier_type) or
            not hours_intersection_check(order.delivery_hours, courier.working_hours) or
            order.region not in courier.regions):
            order.available = True
            order.courier_id = None

        new_orders.append(order_id)

        db.session.commit()

    courier.current_orders = new_orders

    db.session.commit()

    return marshal(courier, _courier_item), 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
