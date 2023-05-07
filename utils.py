import json
import datetime
import pytz
import re

def mask_account_number(account_number):
    if account_number is None:
        return None
    elif len(account_number) >= 4:
        return '**' + account_number[-4:]
    else:
        return '**' + account_number[-1:]

def extract_card_number(description, from_, masked=False):
    """Извлекает номер карты или номер счета из описания операции"""
    if "Maestro" in from_ or "Visa Classic" in from_:
        card_number = from_.replace("Maestro ", "").replace("Visa Classic ", "")
        for i in range(len(card_number)):
            if not card_number[i].isdigit():
                card_number = card_number[:i]
                break
        if masked:
            card_number = mask_card_number(card_number)
        else:
            card_number = f"{card_number[:4]} {card_number[4:5]} {card_number[6:11].replace(card_number[6:11], '*'*4)} {card_number[-4:]}"
        if "Maestro" in from_:
            return f"Maestro {card_number}"
        elif "Visa Classic" in from_:
            return f"Visa Classic {card_number}"
    elif "Счет" in from_:
        account_number = from_.replace('Счет ', '').replace('счет ', '')
        if masked:
            card_number = mask_account_number(account_number)
        else:
            card_number = f"**{account_number[-4:]}"
        return f"Счёт {card_number}"
    else:
        return None


def mask_card_number(card_number):
    """Маскирует номер карты"""
    def mask_card_number(card_number):
        """Маскирует номер карты"""
    if card_number is None:
        raise TypeError("Invalid input type. Expecting a string.")
    if not isinstance(card_number, str):
        raise TypeError("Invalid input type. Expecting a string.")
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Invalid card number format. Expecting a 16-digit numeric string.")
    return f"{card_number[:4]} {card_number[4:6]}** {'*' * 4} {card_number[-4:]}"



def print_last_operations():
    """Выводит информацию о последних 5 выполненных операциях"""
    with open('operations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    executed_operations = [op for op in data if 'state' in op and op['state'] == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=lambda op: op['date'], reverse=True)
    last_five_operations = sorted_operations[:5]
    tz = pytz.timezone('Europe/Moscow')
    for op in last_five_operations:
        date_str = op['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.utc).astimezone(tz)
        description = op['description']
        from_ = op.get('from', '')
        to = op['to']
        amount, currency = op['operationAmount']['amount'], op['operationAmount']['currency']
        if "Maestro" in from_ or "Visa Classic" in from_ or "Счет" in from_.lower():
            card_number = extract_card_number(description, from_, masked=True)
        else:
            card_number = extract_card_number(description, from_)
        masked_to = mask_account_number(to)
        if not from_:
            masked_from = mask_account_number(to)
        else:
            masked_from = card_number
        print(f"{date.strftime('%d.%m.%Y')} {description}")
        print(f"{masked_from} -> {masked_to}")
        print(f"{amount} {currency['name']}\n")

if __name__ == '__main__':
    print_last_operations()
