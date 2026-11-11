# Purpose: Unit test to check that message creation is possible

from app.models.message import Message

def test_message_creation():
    # Arrange: create a message
    message = Message(content="Hello Jomini Library!")

    # Assert: verify the message was created correctly
    assert message.content == "Hello Jomini Library!"
    assert message.id is None
