import pytest
from nosopy import NosoNodeInfo

@pytest.fixture
def elements():
    return [
        'NODESTATUS', # Ignore
        3,            # Peers
        1024,         # Block
        0,            # Pending
        0,            # Sync Delta
        'BRANCH',     # Branch
        'Version'     # Version
    ]

def test_NosoNodeInfo_no_args():
    ni = NosoNodeInfo()

    assert ni.peers == -1
    assert ni.block == -1
    assert ni.pending == -1
    assert ni.sync_delta == -1
    assert ni.branch == 'NONE'
    assert ni.version == 'UNKNOWN'

def test_NosoNodeInfo_with_args(elements):
    ni = NosoNodeInfo(*elements)

    assert ni.peers == 3
    assert ni.block == 1024
    assert ni.pending == 0
    assert ni.sync_delta == 0
    assert ni.branch == 'BRANCH'
    assert ni.version == 'Version'
