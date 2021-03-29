from flask_restplus import Namespace, fields
from .enums import CourierTypeEnum


class CourierDto:
    api = Namespace("couriers", description="couriers related requests")

    courier_item = api.model("CourierItem", {
        "courier_id": fields.Integer(required=True, description="courier unique ID"),
        "courier_type": fields.String(required=True, enum=CourierTypeEnum.member_names_, description="courier type"),
        "regions": fields.List(fields.Integer, required=True, description="regions IDs list"),
        "working_hours": fields.List(fields.String, required=True, description="working hours list")
    })

    courier_post_request = api.model("CourierPostRequest", {
        "data": fields.List(fields.Nested(courier_item), required=True, description="list of courier items")
    })

    courier_get_response_with_rating = api.model("CourierGetResponse", {
        "courier_id": fields.Integer(required=True, description="courier unique ID"),
        "courier_type": fields.String(required=True, enum=CourierTypeEnum.member_names_, description="courier type"),
        "regions": fields.List(fields.Integer, required=True, description="regions IDs list"),
        "working_hours": fields.List(fields.String, required=True, description="working hours list"),
        "rating": fields.Fixed(decimals=2, required=True, description="courier rating"),
        "earnings": fields.Integer(required=True, description="courier earnings")
    })

    courier_get_response = api.model("CourierGetResponse", {
        "courier_id": fields.Integer(required=True, description="courier unique ID"),
        "courier_type": fields.String(required=True, enum=CourierTypeEnum.member_names_, description="courier type"),
        "regions": fields.List(fields.Integer, required=True, description="regions IDs list"),
        "working_hours": fields.List(fields.String, required=True, description="working hours list"),
        "earnings": fields.Integer(required=True, description="courier earnings")
    })

    courier_update_request = api.model("CourierUpdateRequest", {
        "courier_id": fields.Integer(description="courier unique ID"),
        "courier_type": fields.String(enum=CourierTypeEnum.member_names_, description="courier type"),
        "regions": fields.List(fields.Integer, description="regions IDs list"),
        "working_hours": fields.List(fields.String, description="working hours list")
    })
