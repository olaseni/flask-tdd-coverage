from flask import Blueprint, jsonify, url_for, request
from . import actions

bp = Blueprint('person', __name__, url_prefix='/person')


@bp.route('/', methods=['POST'])
def add():
    """
    Adds a person, returns the `id` and new uri of the person
    :return:
    """

    p = request.json
    pid = actions.add_person(
        first_name=p['first_name'],
        last_name=p['last_name'],
        email=p['email'],
        phone=p['phone'],
        date_of_birth=p['date_of_birth'],
        profession=p['profession'],
        address=p['address'],
        notes=p['notes']
    )

    return jsonify({
        'id': pid,
        'uri': url_for('person.view', id=pid)
    })


@bp.route('/', methods=['GET'])
def list():
    """
    Returns persons
    :return:
    """
    return jsonify(actions.list_persons())


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """
    Returns a person view
    :return:
    """
    person = actions.view_person(id)
    return jsonify(person) if person else jsonify({}), 404


@bp.route('/<int:id>', methods=['PUT'])
def edit(id):
    """
    Updates a person resource
    :return:
    """
    if not actions.view_person(id):
        return jsonify({}), 404

    p = request.json
    actions.edit_person(
        id=id,
        first_name=p['first_name'],
        last_name=p['last_name'],
        email=p['email'],
        phone=p['phone'],
        date_of_birth=p['date_of_birth'],
        profession=p['profession'],
        address=p['address'],
        notes=p['notes']
    )
    return jsonify({}), 204


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Deletes a person resource
    :return:
    """
    if not actions.view_person(id):
        return jsonify({}), 404

    actions.remove_person(id)
    return jsonify({}), 204
