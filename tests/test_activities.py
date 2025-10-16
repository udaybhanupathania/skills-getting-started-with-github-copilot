from fastapi.testclient import TestClient
from src import app as application


@property
def client():
    return TestClient(application.app)


def test_signup_and_get_updates():
    client = TestClient(application.app)

    # Ensure test participant is not present
    resp = client.get('/activities')
    assert resp.status_code == 200
    activities = resp.json()
    assert 'tester_integration@mergington.edu' not in activities['Chess Club']['participants']

    # Sign up participant
    resp2 = client.post('/activities/Chess%20Club/signup?email=tester_integration@mergington.edu')
    assert resp2.status_code == 200
    assert 'Signed up tester_integration@mergington.edu for Chess Club' in resp2.json().get('message', '')

    # Immediately GET activities and verify participant appears
    resp3 = client.get('/activities')
    assert resp3.status_code == 200
    activities_after = resp3.json()
    assert 'tester_integration@mergington.edu' in activities_after['Chess Club']['participants']

    # Cleanup: unregister
    resp4 = client.delete('/activities/Chess%20Club/participants?email=tester_integration@mergington.edu')
    assert resp4.status_code == 200
    assert 'Unregistered tester_integration@mergington.edu from Chess Club' in resp4.json().get('message', '')


def test_unregister_nonexistent():
    client = TestClient(application.app)

    # Try to remove a user that isn't signed up
    resp = client.delete('/activities/Chess%20Club/participants?email=not_real@mergington.edu')
    assert resp.status_code == 404
