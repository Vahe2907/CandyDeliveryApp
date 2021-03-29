import datetime

from app.main import db
from app.main.models.couriers import Courier
from app.main.models.orders import Order

from ..util.handlers import parse_interval, compatible, get_date_object, get_date_string, withdraw
from ..util.handlers import hours_intersection_check


def save_new_order(data):
    order = Order.query.filter_by(order_id=data["order_id"]).first()

    if order:
        return data["order_id"], 1

    new_order = Order(
        order_id=data["order_id"],
        weight=data["weight"],
        region=data["region"],
        delivery_hours=data["delivery_hours"],
        available=True,
        courier_id=None
    )

    for interval in new_order.delivery_hours:
        res = parse_interval(interval)
        if res["status"]:
            return new_order.order_id, 1

    if new_order.weight < 0.01 or new_order.weight > 50:
        return new_order.order_id, 1

    save_changes(new_order)

    return data["order_id"], 0


def save_new_orders(data):
    succeed_ids = []
    fail_ids = []

    for micro_data in data:
        order_id, state = save_new_order(micro_data)
        if state:
            fail_ids.append({"id": order_id})
        else:
            succeed_ids.append({"id": order_id})

    if fail_ids:
        response_object = {
            "validation_error": {
                "orders": fail_ids
            }
        }

        return response_object, 400

    response_object = {
        "orders": succeed_ids
    }

    return response_object, 201


def assign_orders(data):
    courier_id = data["courier_id"]

    courier = Courier.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return None, 400

    result = {"orders": []}

    for region_id in courier.regions:
        orders = Order.query.filter_by(region=region_id)
        for order in orders:
            if not order.available:
                continue

            if not compatible(order.weight, courier.courier_type):
                continue

            if not hours_intersection_check(order.delivery_hours, courier.working_hours):
                continue

            courier.current_orders.append(order.order_id)

            order.available = False
            order.courier_id = courier_id

            result["orders"].append({"id": order.order_id})

            db.session.commit()

    if result["orders"]:
        if courier.assign_time is not None:
            result["assign_time"] = courier.assign_time
        else:
            courier.assign_time = get_date_string(datetime.datetime.now())
            courier.checkpoint = courier.assign_time
            result["assign_time"] = courier.assign_time

    db.session.commit()

    return result, 200


def complete_order(data):
    courier_id = data["courier_id"]
    order_id = data["order_id"]

    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return None, 400
    courier = Courier.query.filter_by(courier_id=courier_id).first()
    if not courier:
        return None, 400

    if order.order_id not in courier.current_orders:
        return None, 400

    if order.available or order.courier_id != courier_id:
        return None, 400

    courier.orders_complete += 1
    courier.earnings += withdraw(courier.courier_type)

    complete_time = get_date_object(data["complete_time"])
    start_time = get_date_object(courier.checkpoint)

    delta = (complete_time - start_time).total_seconds()
    if order.region not in courier.average_times:
        courier.average_times[order.region] = [delta]
    else:
        courier.average_times[order.region].append(delta)

    courier.checkpoint = get_date_string(complete_time)

    courier.current_orders.remove(order.order_id)

    db.session.commit()

    return {"order_id": order.order_id}, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
