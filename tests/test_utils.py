import pytest
import json
from utils import mask_account_number, extract_card_number, mask_card_number, print_last_operations
import unittest

class TestMaskAccountNumber(unittest.TestCase):

    def test_masking(self):
        # Test masking with account number greater or equal to 4
        self.assertEqual(mask_account_number('1234567890'), '**7890')
        self.assertEqual(mask_account_number('1234'), '**1234')

        # Test masking with account number less than 4
        self.assertEqual(mask_account_number('123'), '**3')
        self.assertEqual(mask_account_number(''), '**')

    def test_edge_cases(self):
        # Test edge cases
        self.assertEqual(mask_account_number(None), None)


class TestMaskCardNumber(unittest.TestCase):

    def test_with_valid_input(self):
        card_number = "1234567812345678"
        masked_number = mask_card_number(card_number)
        expected_output = "1234 56** **** 5678"
        self.assertEqual(masked_number, expected_output)

    def test_with_non_numeric_input(self):
        with self.assertRaises(ValueError):
            mask_card_number("1234-5678-1234-5678")

    def test_with_incorrect_length_input(self):
        with self.assertRaises(ValueError):
            mask_card_number("12345678")

    def test_with_empty_input(self):
        with self.assertRaises(ValueError):
            mask_card_number("")

    def test_with_none_input(self):
        with self.assertRaises(TypeError):
            mask_card_number(None)

    def test_with_invalid_input_type(self):
        with self.assertRaises(TypeError):
            mask_card_number(1234567812345678)


class TestPrintLastOperations(unittest.TestCase):

    def test_with_empty_file(self):
        # Тестирование функции на случай, когда файл 'operations.json' пустой
        with open('../operations.json', 'w', encoding='utf-8') as f:
            f.write('')
        with self.assertRaises(Exception):
            print_last_operations()

    def test_with_invalid_json(self):
        # Тестирование функции на случай, когда файл 'operations.json' содержит невалидный JSON
        with open('../operations.json', 'w', encoding='utf-8') as f:
            f.write('{"foo": "bar",}')
        with self.assertRaises(Exception):
            print_last_operations()


class TestExtractCardNumber(unittest.TestCase):

    def test_extract_maestro_card_number_with_masking(self):
        description = "Transaction on Maestro card"
        from_ = "Maestro 1234567890123456"
        masked = True
        expected_output = "Maestro 1234 56** **** 3456"
        self.assertEqual(extract_card_number(description, from_, masked), expected_output)

    def test_extract_visa_classic_card_number_without_masking(self):
        description = "Transaction on Visa Classic card"
        from_ = "Visa Classic 1111222233334444"
        masked = False
        expected_output = "Visa Classic 1111 2 **** 4444"
        self.assertEqual(extract_card_number(description, from_, masked), expected_output)

    def test_extract_account_number_with_masking(self):
        description = "Transaction on account"
        from_ = "Счет 12345678901234567890"
        masked = True
        expected_output = "Счёт **7890"
        self.assertEqual(extract_card_number(description, from_, masked), expected_output)

    def test_no_card_or_account_number_present(self):
        description = "Transaction without card or account number"
        from_ = "Some other information"
        masked = False
        expected_output = None
        self.assertEqual(extract_card_number(description, from_, masked), expected_output)

if __name__ == '__main__':
    unittest.main()



