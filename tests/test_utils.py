import pytest
import json
from utils import mask_account_number, extract_card_number, mask_card_number, print_last_operations


@pytest.mark.parametrize('account_number, masked_account_number', [
    ('1234567890123456', '**3456'),
    ('', '**'),
    ('123', '**3'),
    ('1', '**1')
])
def test_mask_account_number(account_number, masked_account_number):
    assert mask_account_number(account_number) == masked_account_number

def test_print_last_operations(capsys):
# Создаем тестовые данные
    data = [
    {
    "description": "Покупка в магазине",
    "from": "40817810099910004302",
    "to": "1234567890123456",
    "operationAmount": {"amount": 500, "currency": {"code": "RUB", "name": "Рубль"}},
    "date": "2023-04-30T12:00:00.000000"
    },
    {
    "description": "Перевод на карту Maestro",
    "from": "40817810099910004302",
    "to": "1234567890123456",
    "operationAmount": {"amount": 1000, "currency": {"code": "RUB", "name": "Рубль"}},
    "date": "2023-04-29T09:00:00.000000"
    },
    {
    "description": "Перевод со счета",
    "from": "40817810099910004302",
    "to": "40817810099910004301",
    "operationAmount": {"amount": 2000, "currency": {"code": "RUB", "name": "Рубль"}},
    "date": "2023-04-28T15:00:00.000000"
    },
    {
    "description": "Оплата услуг",
    "to": "40817810099910004302",
    "operationAmount": {"amount": 3000, "currency": {"code": "RUB", "name": "Рубль"}},
    "date": "2023-04-27T13:00:00.000000"
    },
    {
    "description": "Пополнение счета",
    "to": "40817810099910004302",
    "operationAmount": {"amount": 5000, "currency": {"code": "RUB", "name": "Рубль"}},
    "date": "2023-04-26T10:00:00.000000"
    }
    ]
    with open('operations.json', 'w') as f:
        json.dump(data, f)


def test_mask_card_number():
    # Проверяем работу функции с разными номерами карт
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert mask_card_number("1111222233334444") == "1111 22** **** 4444"
    assert mask_card_number("5555666677778888") == "5555 66** **** 8888"



