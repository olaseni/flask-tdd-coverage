"""
Unit tests for endpoints
"""
from datetime import date
from json import dumps

"""
Useful parameters
"""
first_name, last_name, email, phone, date_of_birth, address, profession, notes = "Boladale", "Efunjobi", \
                                                                                 "boladale.efunjobi@fanatic.co.uk", \
                                                                                 "+234809766543", '%s' % date.today(), \
                                                                                 "Boladale Close", "Musician", None


def add_default_person(client):
    """
    Create an initial user
    """
    return client.post('/person/', data=dumps({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'date_of_birth': date_of_birth,
        'address': address,
        'profession': profession,
        'notes': notes}),
                       content_type='application/json', follow_redirects=True)


def test_list_persons_endpoint_no_init(app_context, client):
    """
    GIVEN an endpoint
    WHEN a GET request is made
    THEN an empty list should be returned as no persons are populated yet
    """
    with app_context():
        response = client.get('/person/')
        assert not response.json
        # random person
        response = client.get('/person/9999')
        assert response.status_code == 404


def test_list_persons_endpoint(app_context, client):
    """
    GIVEN an endpoint
    WHEN a list request is made
    THEN a non-empty list should be returned as one person has been created
    """
    with app_context():
        add_default_person(client)
        response = client.get('/person/', follow_redirects=True)
        assert response.json
        assert len(response.json) == 1


def test_add_and_view_person_endpoint(app_context, client):
    """
    GIVEN an endpoint
    WHEN a person is added
    THEN a subsequent read of that person by id should yield an expected view
    """
    with app_context():
        response = add_default_person(client)
        pid = response.json.get('id', 0)
        response = client.get('/person/%d' % pid, follow_redirects=True)
        assert response.json['first_name'] == first_name
        assert response.json['last_name'] == last_name
        assert response.json['email'] == email
        assert response.json['phone'] == phone
        assert response.json['date_of_birth'] == date_of_birth
        assert response.json['address'] == address
        assert response.json['profession'] == profession
        assert response.json['notes'] == notes


def test_edit_person_endpoint(app_context, client):
    """
    GIVEN an endpoint
    WHEN a request is made to update an existing person
    THEN a subsequent read request on that person should be consistent with the updated changes
    """
    with app_context():
        response = add_default_person(client)
        pid = response.json.get('id', 0)
        response = client.get('/person/%d' % pid, follow_redirects=True)
        person = response.json
        client.put('/person/%d' % pid, follow_redirects=True,
                   content_type='application/json',
                   data=dumps({
                       'first_name': first_name + '-XXX',
                       'last_name': last_name + '-YYY',
                       'email': person['email'],
                       'phone': person['phone'],
                       'date_of_birth': person['date_of_birth'],
                       'address': person['address'],
                       'profession': person['profession'],
                       'notes': person['notes']})
                   )
        response = client.get('/person/%d' % pid, follow_redirects=True)
        assert response.json['first_name'] == first_name + '-XXX'
        assert response.json['last_name'] == last_name + '-YYY'


def test_remove_person_endpoint(app_context, client):
    """
    GIVEN an endpoint
    WHEN a DELETE request is made
    THEN a subsequent read request on that person should return nothing
    """
    with app_context():
        response = add_default_person(client)
        pid = response.json.get('id', 0)
        response = client.get('/person/%d' % pid, follow_redirects=True)
        assert response.json['first_name'] == first_name
        client.delete('/person/%d' % pid, follow_redirects=True)
        response = client.get('/person/%d' % pid, follow_redirects=True)
        assert not response.json
