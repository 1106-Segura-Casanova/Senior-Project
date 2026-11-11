# Purpose: Unit test to check that message valdation and response schemas work

from app.schemas.message_schema import (
    MessageCreate,
    MessageUpdate,
    MessageResponse
)

from app.models.message import Message

def test_message_create_schema():
    message = MessageCreate(content="Hello Jomini Library!")

    assert message.content == "Hello Jomini Library!"

def test_message_update_schema():
    message = MessageUpdate(content="Updated message")

    assert message.content == "Updated message"

def test_message_response_schema():
    # Arrange: create a SQLAlchemy model instance
    message = Message(
        id=1,
        content="Hello Jomini Library!"
    )

    # Act: convert the model into a response schema
    response = MessageResponse.model_validate(message)

    # Assert: verify the response fields
    assert response.id == 1
    assert response.content == "Hello Jomini Library!"
