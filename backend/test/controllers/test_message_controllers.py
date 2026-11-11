# Purpose: Unit test to check if FastAPI is working properly using TestClient and MagicMock -> also makes sure that users cannot access or modify the messages of another user

from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.models.message import Message
from app.models.user import User

# --------------------------------------------------
# MOCK DATABASE AND AUTHENTICATION
# --------------------------------------------------

mock_db = MagicMock()
test_user = User(
    id=1,
    firebase_uid="test-firebase-uid",
    email="test@example.com",
)

test_message = Message(
    id=1,
    content="Hello Jomini Library!",
    user_id=1,
)

def override_get_db():
    yield mock_db


def override_get_current_user():
    return test_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)

# --------------------------------------------------
# TEST RESET
# --------------------------------------------------

def reset_mock_db():
    mock_db.reset_mock()
    mock_db.refresh.side_effect = None
    test_message.content = "Hello Jomini Library!"


# --------------------------------------------------
# OWNERSHIP ASSERTION
# --------------------------------------------------

def assert_message_query_checks_ownership(message_id):
    filters = mock_db.query.return_value.filter.call_args.args

    # Query must filter by both message ID and user ID.
    assert len(filters) == 2

    assert filters[0].left.key == "id"
    assert filters[0].right.value == message_id

    assert filters[1].left.key == "user_id"
    assert filters[1].right.value == test_user.id


# --------------------------------------------------
# GET ALL MESSAGES
# --------------------------------------------------

def test_get_messages():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.all.return_value = [
        test_message
    ]
# Implemented from FastAPI test https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/app_testing/app_b/test_main.py#L8-L15
    response = client.get("/api/messages/")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "content": "Hello Jomini Library!",
        }
    ]

    # Verify that the query filters by the authenticated user.
    filters = mock_db.query.return_value.filter.call_args.args

    assert len(filters) == 1
    assert filters[0].left.key == "user_id"
    assert filters[0].right.value == test_user.id


# --------------------------------------------------
# CREATE MESSAGE
# --------------------------------------------------

def test_create_message():
    reset_mock_db()

    def mock_refresh(message):
        message.id = 2

    mock_db.refresh.side_effect = mock_refresh
# Took from FastAPI testing https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/app_testing/app_b/test_main.py#L30-L41
    response = client.post(
        "/api/messages/",
        json={
            "content": "Testing POST functionality!"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 2,
        "content": "Testing POST functionality!",
    }

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    added_message = mock_db.add.call_args.args[0]

    assert added_message.content == "Testing POST functionality!"
    assert added_message.user_id == test_user.id


# --------------------------------------------------
# GET MESSAGE BY ID
# --------------------------------------------------

def test_get_message_by_id():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = (
        test_message
    )

    response = client.get("/api/messages/1")

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "content": "Hello Jomini Library!",
    }

    assert_message_query_checks_ownership(1)


# --------------------------------------------------
# GET MESSAGE NOT FOUND
# --------------------------------------------------

def test_get_message_not_found():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get("/api/messages/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(999)


# --------------------------------------------------
# UPDATE MESSAGE
# --------------------------------------------------

def test_update_message():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = (
        test_message
    )

    response = client.put(
        "/api/messages/1",
        json={
            "content": "Updated Jomini Library message!"
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "content": "Updated Jomini Library message!",
    }

    assert test_message.content == "Updated Jomini Library message!"

    assert_message_query_checks_ownership(1)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(test_message)


# --------------------------------------------------
# UPDATE MESSAGE NOT FOUND
# --------------------------------------------------

def test_update_message_not_found():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.put(
        "/api/messages/999",
        json={
            "content": "Updated message"
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(999)

    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()


# --------------------------------------------------
# DELETE MESSAGE
# --------------------------------------------------

def test_delete_message():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = (
        test_message
    )

    response = client.delete("/api/messages/1")

    assert response.status_code == 200

    assert response.json() == {
        "detail": "Message deleted"
    }

    assert_message_query_checks_ownership(1)

    mock_db.delete.assert_called_once_with(test_message)
    mock_db.commit.assert_called_once()


# --------------------------------------------------
# DELETE MESSAGE NOT FOUND
# --------------------------------------------------

def test_delete_message_not_found():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.delete("/api/messages/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(999)

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


# --------------------------------------------------
# CROSS-USER SECURITY TESTS
# --------------------------------------------------

def test_user_cannot_read_another_users_message():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get("/api/messages/2")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(2)


def test_user_cannot_update_another_users_message():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.put(
        "/api/messages/2",
        json={
            "content": "Unauthorized update"
        },
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(2)

    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()


def test_user_cannot_delete_another_users_message():
    reset_mock_db()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.delete("/api/messages/2")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Message not found"
    }

    assert_message_query_checks_ownership(2)

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

def teardown_module():
    app.dependency_overrides.clear()

