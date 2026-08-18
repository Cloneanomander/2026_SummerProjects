import hashlib,json,sys,random
def hashme(msg=""):
    if type(msg) != str:
        msg = json.dumps(msg,sort_keys=True)
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
def makeTansaction(maxValue=3):
    sign = int(random.getrandbits(1))*2
    amount = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays = -1 *alicePays
    return {u'Alice':alicePays,u'Bob':bobPays}
txnBuffer = [makeTansaction() for _ in range(30)]
def updateState(txn,state):
    state = state.copy()
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        state[key] = txn[key]
    return state
def isvalidTxn(txn,state):
    if sum(txn.values()) != 0:
        return False
    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctbalance = 0
        if(acctBalance + txn[key]) < 0:
            return False
    return True
state = {u'Alice':5,u'Bob':5}
print(isvalidTxn({u'Alice': -3, u'Bob': 3},state))
state = {u'Alice':50,u'Bob':50}
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashme(genesisBlockContents)
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock,sort_keys=True)
chain = [genesisBlock]
def makeBlock(txns,chain):
    parentBlock = chain[-1]
    parentHash = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    txnCount = len(txns)
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,u'txnCount':len(txns),'txns':txns}
    blockHash = hashme(blockContents)
    block = {u'hash':blockHash,u'contents':blockContents}
    return block
blockSizeLimit = 5
