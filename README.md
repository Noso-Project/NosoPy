# NosoPy

Set of classes and tools to communicate with a Noso wallet using NosoP(Noso Protocol).

The data that can be retrieved consist of:

- Node information
- Pool information

Since this coin's protocol is transistion from version 1(P1) to version 2(P2), this will probably be a short lived repository.

## Instruction for use

### Node Info

```py
from nosopy import NosoNode

node = NosoNode('Win1', '192.210.226.118', 8080)
node_info = node.get_info()
if node_info is not None:
    print(f'Node: "{node.name}" {node.host}:{node.port}')
    print('  Peers:', node_info.peers)
    print('  Block:', node_info.block)
    print('  Pending:', node_info.pending)
    print('  Sync Delta:', node_info.sync_delta)
    print('  Branch:', node_info.branch)
    print('  Version:', node_info.version)
else:
    print('Something went wrong while retreiving the NodeInfo')
```

### Pool Info

```py
from nosopy import NosoPool

pool = NosoPool('ITBPool', '2.tcp.ngrok.io', 11687, 'Password')
pool_info = pool.get_info('gcarreno-main')

print(f'Pool: "{pool.name}" {pool.host}:{pool.port} "{pool.password}"')
print(f'  Hash rate: {pool_info.hash_rate}')
print( '  Fee:', str(pool_info.fee/100) + '%')
print(f'  Share: {pool_info.share}%')
if pool_info.miners_count > 0:
    print(f'  Miners: {pool_info.miners_count}')
    for miner in pool_info.miners:
        print(f'Address: {miner.address}')
        print(f'Balance: {miner.balance}')
        print(f'Blocks: {miner.blocks_until_payment}')
        print('------------------')
```
