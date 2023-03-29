import sys
import pytest
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from lambda_function import generate_reply

@pytest.fixture
def load_env():
    from dotenv import load_dotenv
    load_dotenv()

def test_generate_reply():
    user_message = "Hello, world!"
    reply = generate_reply(user_message)
    assert isinstance(reply, str)
