import time
import uuid
from typing import Dict, List, Any


# TODO: 1. Define Custom Exceptions
class InsufficientBalanceError(Exception):
    pass
    

class InsufficientAllowanceError(Exception):
    pass

class UnauthorizedError(Exception):
    pass


# TODO: 2. Implement TokenTransaction
class TokenTransaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.tx_hash = f"0x{uuid.uuid4().hex[:8]}"
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.strftime("%H:%M:%S")

    def __str__(self) -> str:
        # Format as [Tx 0x1234abcd | Alice -> Bob | 100.00 TK]
        trans_hist = f"[tx {self.tx_hash} | {self.sender} -> {self.recipient} | {self.amount:.2f} TK]"
        return trans_hist


# TODO: 3. Implement ERC20Token
class ERC20Token:
    def __init__(self, name: str, symbol: str, owner: str):
        self.name = name
        self.symbol = symbol
        self.owner = owner
        self._balances: Dict[str, float] = {}
        self._allowances: Dict[str, Dict[str, float]] = {}
        self.history: List[TokenTransaction] = []

    def balance_of(self, account: str) -> float:
        return self._balances.get(account, 0.0)

    def mint(self, to_account: str, amount: float, caller: str) -> None:
        # Check permissions & mint
        if caller != self.owner:
            raise UnauthorizedError("You are not allowed.")
        else:
            self._balances[to_account] = self._balances.get(to_account,0.0) + amount
        

    def transfer(self, sender: str, recipient: str, amount: float) -> TokenTransaction:
        # Check balance, update state, return receipt
        if amount > self.balance_of(sender):
            raise InsufficientBalanceError("You don't have enough balance.")
        self._balances[sender] -= amount
        self._balances[recipient] = self.balance_of(recipient) + amount
        tx = TokenTransaction(sender, recipient, amount)
        self.history.append(tx)
        return tx

    def approve(self, owner: str, spender: str, amount: float) -> None:
        # Set allowance mapping
        if owner not in self._allowances:
            self._allowances[owner] = {}
        self._allowances[owner][spender] = amount

    def transfer_from(self, spender: str, owner: str, recipient: str, amount: float) -> TokenTransaction:
        # Check balance AND allowance, update both, update recipient balance
        if self.balance_of(owner) < amount:
            raise InsufficientBalanceError(f"{self.owner} don't have enough balance.")
        owner_allowance = self._allowances.get(owner,{})
        current_allowance = owner_allowance.get(spender,0.0)
        if current_allowance < amount:
            raise InsufficientAllowanceError(f"{spender} is only allowed to spend {current_allowance}.")
        self._allowances[owner][spender] -= amount
        self._balances[owner] -= amount
        self._balances[recipient] += amount
        return TokenTransaction(owner,recipient,amount)

        


# TODO: 4. Implement StakingVault
class StakingVault:
    def __init__(self, token: ERC20Token, apy: float = 0.10):
        self.token = token
        self.apy = apy
        self.staked_balances: Dict[str, float] = {}
        self.vault_address = "VAULT_CONTRACT"

    def stake(self, user: str, amount: float) -> None:
        # Must call self.token.transfer_from()
        self.token.transfer_from(
            spender=self.vault_address, 
            owner=user, 
            recipient=self.vault_address, 
            amount=amount
        )
        self.staked_balances[user] = self.staked_balances.get(user, 0.0) + amount
    def distribute_yield(self, user: str) -> None:
        # Calculate yield and transfer to user
        earned_interest = self.staked_balances.get(user, 0.0) * self.apy
        self.token.mint(to_account=user, amount=earned_interest, caller=self.token.owner)
        

    @classmethod
    def from_config(cls, token: ERC20Token, config: Dict[str, Any]):
        return cls(token=token, apy=config.get("apy", 0.05))


if __name__ == "__main__":
    print("=== STARTING PROTOCOL TEST SUITE ===")
    
    # Setup
    token = ERC20Token(name="Ether", symbol="ETH", owner="Alice")
    vault = StakingVault(token=token, apy=0.20)  # 20% APY
    
    # Test 1: Minting & Security
    token.mint("Alice", 1000.0, caller="Alice")
    assert token.balance_of("Alice") == 1000.0, "Minting failed!"
    
    try:
        token.mint("Bob", 500.0, caller="Bob")
        print("❌ Test 1 Failed: Unauthorized user minted tokens!")
    except UnauthorizedError:
        print("✓ Test 1 Passed: Unauthorized mint correctly blocked.")

    # Test 2: Direct Transfer & Overspending
    tx1 = token.transfer("Alice", "Bob", 200.0)
    assert token.balance_of("Alice") == 800.0
    assert token.balance_of("Bob") == 200.0
    
    try:
        token.transfer("Bob", "Alice", 9999.0)
        print("❌ Test 2 Failed: Overspending allowed!")
    except InsufficientBalanceError:
        print("✓ Test 2 Passed: Overspending blocked.")

    # Test 3: Unapproved Vault Staking
    try:
        vault.stake("Bob", 100.0)
        print("❌ Test 3 Failed: Staked without approval!")
    except InsufficientAllowanceError:
        print("✓ Test 3 Passed: Unapproved staking attempt blocked.")

    # Test 4: Approved Staking Flow
    token.approve(owner="Bob", spender=vault.vault_address, amount=100.0)
    vault.stake("Bob", 100.0)
    assert token.balance_of("Bob") == 100.0
    assert token.balance_of(vault.vault_address) == 100.0
    assert vault.staked_balances["Bob"] == 100.0
    print("✓ Test 4 Passed: Allowance & Staking flow verified.")

    # Test 5: Yield Distribution
    vault.distribute_yield("Bob")
    # 20% of 100 staked = 20 tokens interest
    assert token.balance_of("Bob") == 120.0
    print("✓ Test 5 Passed: Yield distribution calculated correctly.")
    
    print("\n🎉 ALL PROTOCOL TESTS PASSED PERFECTLY!")

    #C:\Users\minor\py\paiza_python_learning.py

