import pytest
from nosopy import NosoPoolInfo

elements = [
    'STATUS', # Ignore
    3,        # Hash rate
    1,        # Fee
    100,      # Share
    2,        # Miners Count
    # Miner 1
    'Naddress1:0:30',
    # Miner 2
    'Naddress2:0:30'
]

def test_NosoPoolInfo_no_args():
    pi = NosoPoolInfo('TestPool')

    assert pi.name == 'TestPool'
    assert pi.hash_rate == -1
    assert pi.fee == -1
    assert pi.share == -1
    assert pi.miners_count == -1
    assert len(pi.miners) == 0

def test_NosoPoolInfo_with_args():
    pi = NosoPoolInfo('TestPool', *elements)

    assert pi.name == 'TestPool'
    assert pi.hash_rate == 3
    assert pi.fee == 1
    assert pi.share == 100
    assert pi.miners_count == 2
    assert len(pi.miners) == 2
