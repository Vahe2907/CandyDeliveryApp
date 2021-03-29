from flask import request
from flask_restplus import Resource
from ..util.courier_dto import CourierDto
from ..services.couriers_services import save_new_couriers, get_courier, update_courier

api = CourierDto.api

_courier_item = CourierDto.courier_item
_courier_post_request = CourierDto.courier_post_request
_courier_get_response = CourierDto.courier_get_response
_courier_update_request = CourierDto.courier_update_request


@api.route("/")
@api.response(201, "Created")
@api.response(400, "Bad request")
class CouriersHandler(Resource):
    @api.doc("Import couriers")
    @api.expect(_courier_post_request, validate=True)
    def post(self):
        """ Import couriers """
        data = request.json["data"]
        return save_new_couriers(data)


@api.route("/<int:courier_id>")
@api.param("courier_id", "The courier ID")
@api.response(404, "Not found")
@api.response(200, "OK")
class Courier(Resource):
    @api.doc("Get courier info")
    def get(self, courier_id):
        """ Get courier info """
        return get_courier(courier_id)

    @api.doc("Update courier by id")
    @api.expect(_courier_update_request, validate=True)
    @api.response(400, "Bad Request")
    def patch(self, courier_id):
        """ Update courier by id """
        data = request.json
        return update_courier(courier_id, data)
