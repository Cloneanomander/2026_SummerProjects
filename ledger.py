from typing import List, Dict, Any

# Initial in-memory data store: a list of transaction dictionaries
transactions: List[Dict[str, Any]] = [
    {"id": 1, "type": "deposit", "amount": 1000.0, "category": "Initial Balance"},
    {"id": 2, "type": "withdrawal", "amount": 50.0, "category": "Food"},
]


def add_transaction(tx_type: str, amount: float, category: str) -> None:
    """Adds a new transaction to the global list with an incremental ID."""
    # TODO: Generate a new ID (e.g., len(transactions) + 1)
    if not transactions:
        new_id = 1
    else:
        new_id = max(tx["id"] for tx in transactions) + 1
    # TODO: Create a dictionary for the new transaction
    new_transactions = {"id": new_id, "type":tx_type, "amount":amount, "category":category}
    # TODO: Append the new transaction to the `transactions` list
    transactions.append(new_transactions)


def calculate_balance() -> float:
    """Calculates total balance (Deposits minus Withdrawals) using list comprehensions or sum()."""
    # TODO: Sum up all deposits
    if not transactions:
        return 0.0
    deposits = sum(tx["amount"] for tx in transactions if tx["type"] == "deposit")
    # TODO: Sum up all withdrawals
    withdrawals = sum(tx["amount"] for tx in transactions if tx["type"] == "withdrawal")
    # TODO: Return (deposits - withdrawals)
    return deposits - withdrawals


def filter_by_category(category_name: str) -> List[Dict[str, Any]]:
    """Returns a list of transactions matching the specified category (case-insensitive)."""
    # TODO: Use a list comprehension to filter matching categories
    return [
        tx for tx in transactions 
        if tx["category"].lower() == category_name.lower()
    ]
    


def display_transactions(tx_list: List[Dict[str, Any]]) -> None:
    """Formats and prints a given list of transactions clearly."""
    if not tx_list:
        print("\n[!] No transactions found.")
        return

    print("\nID  | Type        | Amount     | Category")
    print("-" * 45)
    for tx in tx_list:
        # Formatted string for alignment
        print(f"{tx['id']:<3} | {tx['type'].capitalize():<11} | ${tx['amount']:<9.2f} | {tx['category']}")


def main() -> None:
    """Main program loop / CLI menu interface."""
    while True:
        print("\n=== PYTHON CLI LEDGER ===")
        print("1. View All Transactions")
        print("2. Add Transaction")
        print("3. Check Current Balance")
        print("4. Filter Transactions by Category")
        print("5. Exit")

        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            display_transactions(transactions)

        elif choice == "2":
            tx_type = input("Enter type (deposit/withdrawal): ").strip().lower()
            if tx_type not in ["deposit", "withdrawal"]:
                print("[!] Invalid type. Must be 'deposit' or 'withdrawal'.")
                continue

            try:
                amount = float(input("Enter amount: $"))
                if amount <= 0:
                    print("[!] Amount must be positive.")
                    continue
            except ValueError:
                print("[!] Invalid number format.")
                continue

            category = input("Enter category (e.g., Food, Salary): ").strip()
            add_transaction(tx_type, amount, category)
            print("[✓] Transaction added successfully!")

        elif choice == "3":
            balance = calculate_balance()
            print(f"\n[💰] Current Net Balance: ${balance:.2f}")

        elif choice == "4":
            cat = input("Enter category to search: ").strip()
            filtered = filter_by_category(cat)
            display_transactions(filtered)

        elif choice == "5":
            print("\nExiting CLI Ledger. Great job on Week 1!")
            break

        else:
            print("[!] Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()