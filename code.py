Code:
budget_enhanced.py
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("data/budget.json")

def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"transactions": []}

def save(state):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(state, indent=2))

def add(tx_type, amount, category, desc, t_date=None):
    st = load()
    tx = {
        "id": max([0]+[t["id"] for t in st["transactions"]])+1,
        "type": tx_type,
        "amount": float(amount) if tx_type=="income" else -abs(float(amount)),
        "category": category,
        "description": desc,
        "date": t_date or date.today().isoformat()
    }
    st["transactions"].append(tx)
    save(st)
    return tx

def summary(year, month):
    st = load()
    total_income = sum(t["amount"] for t in st["transactions"] if t["type"]=="income" and t["date"].startswith(f"{year}-{str(month).zfill(2)}"))
    total_expense = sum(-t["amount"] for t in st["transactions"] if t["type"]=="expense" and t["date"].startswith(f"{year}-{str(month).zfill(2)}"))
    net = total_income - total_expense
    return {"income": total_income, "expense": total_expense, "net": net}

def main():
    print("Enhanced Budget Tracker")
    while True:
        print("\nOptions: 1)add 2)summary 3)exit")
        ch = input("Choose: ").strip()
        if ch=="1":
            ttype = input("Type (income/expense): ").strip().lower()
            amt = float(input("Amount: "))
            cat = input("Category: ")
            desc = input("Description: ")
            d = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
            add(ttype, amt, cat, desc, d or None)
            print("Added.")
        elif ch=="2":
            y = int(input("Year: "))
            m = int(input("Month (1-12): "))
            s = summary(y, m)
            print(f"Income: {s['income']:.2f}, Expense: {s['expense']:.2f}, Net: {s['net']:.2f}")
        elif (ch=="3"):
            break
        else:
            print("Invalid.")

if __name__ == "__main__":
    main()
