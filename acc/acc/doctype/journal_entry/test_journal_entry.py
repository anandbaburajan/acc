# Copyright (c) 2022, Anand and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.exceptions import ValidationError


class TestJournalEntry(FrappeTestCase):
    def test_valid_journal_entry(self):
        journal_entry = frappe.get_doc({
            'doctype': 'Journal Entry',
            'date': '2022-08-23',
            'description': 'Employee Salary',
            'debit_account': 'Indirect Expenses',
            'debit_amount': 4200,
            'credit_account': 'Current Assets',
            'credit_amount': 4200
        })

        journal_entry.insert()

        self.assertTrue(frappe.db.exists('Journal Entry', journal_entry.name))

    def test_invalid_journal_entry(self):
        journal_entry = frappe.get_doc({
            'doctype': 'Journal Entry',
            'date': '2022-08-23',
            'description': 'Employee Salary',
            'debit_account': 'Indirect Expenses',
            'debit_amount': 4200,
            'credit_account': 'Current Assets',
            'credit_amount': 9300
        })

        self.assertRaises(ValidationError, journal_entry.insert)
