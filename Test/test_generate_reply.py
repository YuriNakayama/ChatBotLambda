import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from lambda_function import generate_reply

def test_generate_reply():
    user_message = "Hello, world!"
    reply = generate_reply(user_message)
    assert isinstance(reply, str)
