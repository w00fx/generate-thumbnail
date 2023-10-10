import pytest
from botocore.stub import Stubber
from handler import s3_client

@pytest.fixture(autouse=True)
def s3_stub():
    with Stubber(s3_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()