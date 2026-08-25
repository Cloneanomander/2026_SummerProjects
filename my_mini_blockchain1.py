import hashlib,json,sys,random,copy
def hashme(msg=""):
    if type(msg) != str:
        msg = json.dumps(msg,sort_keys=True)
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
def makeTransaction(maxValue=3):
    sign = int(random.getrandbits(1))*2
    amount = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays = -1 *alicePays
    return {u'Alice':alicePays,u'Bob':bobPays}
txnBuffer = [makeTransaction() for _ in range(30)]
def updateState(txn,state):
    state = state.copy()
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state
def isvalidTxn(txn,state):
    if sum(txn.values()) != 0:
        return False
    for key in txn.keys():
        if key in state.keys():
            acctbalance = state[key]
        else:
            acctbalance = 0
        if(acctbalance + txn[key]) < 0:
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
    blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash,u'txnCount':len(txns),'txns':list(txns)}
    blockHash = hashme(blockContents)
    block = {u'hash':blockHash,u'contents':blockContents}
    return block
blockSizeLimit = 5

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    #Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) and (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isvalidTxn(newTxn,state)
        #This will return False if txn is invalid
        if validTxn:
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue
    #Make a block
    myBlock = makeBlock(txnList,chain)
    chain.append(myBlock)

def checkBlockHash(block):
    #Raise an exception if the hash does not match the block contents
    expectedHash = hashme(block['contents'])
    if block['hash'] != expectedHash:
        raise Exception('Hash does not match contents of block %s'%block['contents']['blockNumber'])
    return

def checkBlockValidity(block,parent,state):
    #We want to check the following conditions:
    #1.Each of the transactions are valid updates to the system state
    #2.Block hash is valid for the block contents
    #3.Block number increments the parent parent block number by 1
    #Accuretly references the parent block's hash
    parentNumber = parent['contents']['blockNumber']
    parentHash = parent['hash']
    blockNumber = block['contents']['blockNumber']
    #Check transaction validity; throw an error if an invalid transaction was found
    for txn in block['contents']['txns']:
        if isvalidTxn(txn,state):
            state = updateState(txn,state)
        else:
            raise Exception(f"Invalid transaction in block {blockNumber}:{txn}")
    checkBlockHash(block)
    if blockNumber != (parentNumber+1):
        raise Exception(f"Hash does not match contents of block {blockNumber}")
    if block['contents']['parentHash'] != parentHash:
        raise Exception(f"Parent hash not accurate at block {blockNumber}")
    return state

def checkChain(chain):
    #Work through the chain from the genesis block
    #checking that all transactions are internally valid
    # that the blocks are linked by their hashes
    #This returns the state as a dictionary of accounts and balances,
    # or returns False if an error was detected
    if type(chain) == str:
        try:
            chain = json.loads(chain)
            assert(type(chain) == list)
        except:
            return False
    elif type(chain) != list:
        return False
    state = {}
    #Prime the pump by checking the genesis block
    for txn in chain[0]['contents']['txns']:
        state = updateState(txn,state)
    checkBlockHash(chain[0])
    parent = chain[0]
    #Checking subsequent blocks: These additionally need to check
    # - the reference to the parent block's hash
    # - the validity of the block number
    for block in chain[1:]:
        state = checkBlockValidity(block,parent,state)
        parent = block
    return state

chainAsText = json.dumps(chain,sort_keys=True)
checkChain(chainAsText)

nodeBchain = copy.copy(chain)
nodeBtxns = [makeTransaction() for i in range(5)]
newBlock = makeBlock(nodeBtxns,nodeBchain)

print(f"Blockchain on Node A is currently {len(chain)} long.")
try:
    print(f"New Block Received; checking validity...")
    state = checkBlockValidity(newBlock,chain[-1],state)
    chain.append(newBlock)
except:
    print(f"Invalid block; ignoring and waiting for the next block...")

print(f"Blockchain on Node A is now {len(chain)}.")


    
    
        
