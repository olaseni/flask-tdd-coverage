"""
Operations related to managing a person entity
"""

from . import persistence


def _cursor():
    return persistence.get_db().cursor()


def add_person(first_name, last_name, email, phone, date_of_birth, address, profession, notes=None):
    """
    Adds a person and returns the id
    :param first_name:
    :param last_name:
    :param email:
    :param phone:
    :param date_of_birth:
    :param address:
    :param profession:
    :param notes:
    :return:
    """

    c = _cursor()
    c.execute(
        'INSERT INTO person (first_name, last_name, email, phone, date_of_birth, address, profession, notes) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (first_name, last_name, email, phone, date_of_birth, address, profession, notes)
    )

    return c.lastrowid


def view_person(id):
    """
    Returns a person from the db by id
    :param id:
    :return:
    """

    return _cursor().execute(
        'SELECT id, first_name, last_name, email, phone, date_of_birth, address, profession, notes '
        'FROM person WHERE id = ?', (id,)).fetchone()


def list_persons():
    """
    Returns a list of `person`s from the db
    """

    return _cursor().execute(
        'SELECT id, first_name, last_name, email, phone, date_of_birth, address, profession, notes '
        'FROM person').fetchall()


def edit_person(id, first_name, last_name, email, phone, date_of_birth, address, profession, notes=None):
    """
    Updates a person's details
    :param id:
    :param first_name:
    :param last_name:
    :param email:
    :param phone:
    :param date_of_birth:
    :param address:
    :param profession:
    :param notes:
    """
    _cursor().execute('UPDATE person SET '
                      ' first_name = ?, last_name = ?, email = ?, phone = ?, '
                      ' date_of_birth = ?, address = ?, profession = ?, notes = ?, '
                      ' modified = datetime("now")'
                      ' WHERE id = ?',
                      (first_name, last_name, email, phone, date_of_birth, address, profession, notes, id,))


def remove_person(id):
    """
    Removes a person from the db by id
    :param id:
    :return:
    """
    _cursor().execute('DELETE FROM person WHERE id = ?', (id,))
