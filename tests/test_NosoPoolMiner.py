import pytest
from nosopy import NosoPoolMiner

@pytest.fixture
def elements():
    return [
        'TestAddress', # Address
        120,           # Balance
        30             # Blocks until payment
    ]

def test_NosoPoolMiner_no_args():
    miner = NosoPoolMiner()

    assert miner.address == ''
    assert miner.balance == -1
    assert miner.blocks_until_payment == -1

def test_NosoPoolMiner_with_args(elements):
    miner = NosoPoolMiner(*elements)

    assert miner.address == 'TestAddress'
    assert miner.balance == 120
    assert miner.blocks_until_payment == 30
