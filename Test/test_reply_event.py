import sys
import pytest
import json
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from lambda_function import lambda_handler, generate_reply

with open ("/var/task/Test/Event/test_event_hello.json") as f:
    user_json = json.load(f)

@pytest.fixture
def load_env():
    from dotenv import load_dotenv
    load_dotenv()

def test_generate_reply():
    # reply = lambda_handler(user_json, {})
    # assert isinstance(reply, str)
    user_message="こんにちは"
    reply = generate_reply(user_message)
    print(reply)

if __name__=="__main__":
    test_generate_reply()