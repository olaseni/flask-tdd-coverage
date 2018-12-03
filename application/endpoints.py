from flask import Blueprint, jsonify, url_for

bp = Blueprint('person', __name__, url_prefix='/person')


@bp.route('/', methods=['POST'])
def add():
    """
    Adds a person, returns the `id` and new uri of the person
    :return:
    """

    return jsonify({
        'id': 0,
        'uri': ''
    })


@bp.route('/', methods=['GET'])
def list():
    """
    Returns persons
    :return:
    """
    return jsonify([{
        'id': id,
        'uri': url_for('person.view', id=id)
    }])


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    """
    Returns a person view
    :return:
    """
    return jsonify({
        'id': id,
        'uri': url_for('person.view', id=id)
    })


@bp.route('/<int:id>', methods=['PUT'])
def edit(id):
    """
    Updates a person resource
    :return:
    """
    return None, 204


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Deletes a person resource
    :return:
    """
    return None, 204
