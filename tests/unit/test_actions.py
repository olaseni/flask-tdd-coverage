"""
Unit tests for actions
"""

from datetime import date
from application import actions

"""
Useful parameters
"""
first_name, last_name, email, phone, date_of_birth, address, profession, notes = "Boladale", "Efunjobi", \
                                                                                 "boladale.efunjobi@fanatic.co.uk", \
                                                                                 "+234809766543", '%s' % date.today(), \
                                                                                 "Boladale Close", "Musician", None


def add_default_person():
    """
    Create an initial user
    """
    return actions.add_person(first_name, last_name, email, phone, date_of_birth, address, profession, notes)


def test_add_person(app_context):
    """
    GIVEN a flask app context
    WHEN a person is added to the db
    THEN check that data added to the db is consistent with user expectation
    """
    with app_context():
        assert add_default_person() == 1
        assert len(actions.list_persons()) == 1
        assert actions.view_person(1)['first_name'] == first_name


def test_view_person(app_context):
    """
    GIVEN a flask app context
    WHEN a person is added to the db
    THEN check that data added to the db is consistent and can be viewed
    """
    with app_context():
        person = actions.view_person(add_default_person())
        assert first_name in person
        assert last_name in person
        assert first_name == person['first_name']
        assert last_name == person['last_name']
        assert email == person['email']
        assert phone == person['phone']
        assert date_of_birth == person['date_of_birth']
        assert address == person['address']
        assert profession == person['profession']
        assert notes == person['notes']


def test_edit_person(app_context):
    """
    GIVEN a flask app context
    WHEN a person is fetched from the db and thereafter updated
    THEN check that updated data is consistent with user expectation
    """
    with app_context():
        person = actions.view_person(add_default_person())
        actions.edit_person(
            person['id'],
            'edited_first_name',
            'edited_last_name',
            person['email'],
            person['phone'],
            person['date_of_birth'],
            person['address'],
            person['profession'],
            person['notes'],
        )
        pid = person['id']
        del person
        person = actions.view_person(pid)
        assert person['first_name'] == 'edited_first_name'
        assert person['last_name'] == 'edited_last_name'
        # ensure no extra person was created
        assert len(actions.list_persons()) == 1


def test_remove_person(app_context):
    """
    GIVEN a flask app context
    WHEN a person is deleted from the db
    THEN check that that person can no longer be viewed
    """
    with app_context():
        pid = add_default_person()
        actions.remove_person(pid)
        assert actions.view_person(pid) is None
        assert len(actions.list_persons()) == 0
