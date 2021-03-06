from flask import request, current_app, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from common.error import SQLCustomError, RequestDataEmpty, ValidateFail
from controller.api import api, post_request_empty
from service.address.address_service import AddressService

address_service = AddressService()


@api.route("/addresses/<int:address_id>", methods=["GET"])
@jwt_required
@cross_origin()
def get_address_by_id(address_id: int):
    """
    get address by id
    :param address_id:
    :return:
    """
    try:
        address = address_service.get_address_by_id(address_id)
        current_app.logger.info("Return data for address_id: {}".format(address_id))
        return jsonify({
            "data": {
                "schools": address
            }}), 200
    except SQLCustomError as error:
        current_app.logger.error("Return error for school_id: {}".format(address_id))
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400


@api.route("/addresses", methods=["POST"])
@jwt_required
@cross_origin()
def create_address():
    """
    create address data
    :return:
    """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        current_app.logger.info("create address")
        address_id = address_service.create_address({
            "division": data.get("division"),
            "district": data.get("district"),
            "township": data.get("township"),
            "street_address": data.get("street_address")
        })
        current_app.logger.info("create address success. address %s", data.get("street_address"))
        return get_address_by_id(address_id)
    except (SQLCustomError, ValidateFail, RequestDataEmpty) as error:
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400


@api.route("/addresses/<int:address_id>", methods=["PUT"])
@jwt_required
@cross_origin()
def update_address(address_id: int):
    """
    update address data
    :param address_id:
    :return:
    """
    data = request.get_json()
    if data is None:
        return post_request_empty()
    try:
        current_app.logger.info("update address for address_id: %s", address_id)
        return jsonify({
            "status": address_service.update_address_by_id(address_id, data)
        }), 200
    except (SQLCustomError, ValidateFail, RequestDataEmpty) as error:
        current_app.logger.error("update address fail: address_id: %s", address_id)
        return jsonify({
            "errors": {
                "error": error.__dict__
            }
        }), 400
