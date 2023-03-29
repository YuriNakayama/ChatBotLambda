def test_generate_reply():
    user_message = "Hello, world!"
    reply = generate_reply(user_message)
    assert isinstance(reply, str)
