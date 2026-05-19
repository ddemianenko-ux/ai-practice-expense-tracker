import argparse
import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_expense(category, amount, description):
    data = load_data()
    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "amount": float(amount),
        "description": description
    }
    data.append(expense)
    save_data(data)
    print(f"Витрату успішно додано!")

def list_expenses(category=None):
    data = load_data()
    if category:
        data = [e for e in data if e["category"] == category]
    
    for e in data:
        print(f"[{e['date']}] {e['category']} - {e['amount']} грн: {e['description']}")

def summarize_expenses():
    data = load_data()
    total = sum(e["amount"] for e in data)
    by_category = defaultdict(float)
    for e in data:
        by_category[e["category"]] += e["amount"]
    
    print(f"Загальна сума витрат: {total} грн")
    print("За категоріями:")
    for cat, amount in by_category.items():
        print(f" - {cat}: {amount} грн")

def main():
    parser = argparse.ArgumentParser(description="CLI-калькулятор витрат")
    subparsers = parser.add_subparsers(dest="command")

    # Команда add
    add_parser = subparsers.add_parser("add", help="Додати витрату")
    add_parser.add_argument("--category", required=True, help="Категорія витрати")
    add_parser.add_argument("--amount", required=True, type=float, help="Сума")
    add_parser.add_argument("--desc", required=True, help="Опис")

    # Команда list
    list_parser = subparsers.add_parser("list", help="Переглянути витрати")
    list_parser.add_argument("--category", help="Фільтр за категорією")

    # Команда summary
    subparsers.add_parser("summary", help="Підрахунок загальної суми")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.category, args.amount, args.desc)
    elif args.command == "list":
        list_expenses(args.category)
    elif args.command == "summary":
        summarize_expenses()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()