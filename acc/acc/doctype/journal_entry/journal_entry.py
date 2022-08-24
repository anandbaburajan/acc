# Copyright (c) 2022, Anand and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JournalEntry(Document):
    def validate(self):
        debit_account = frappe.get_doc("Account", self.debit_account)
        credit_account = frappe.get_doc("Account", self.credit_account)

        if debit_account.is_group or credit_account.is_group:
            frappe.throw("Cannot debit/credit a group account.")

        if self.debit_amount != self.credit_amount:
            frappe.throw("Debit amount should be equal to credit amount.")

    def after_insert(self):
        name = self.name + "-debit"
        self.create_ledger_entry(
            "debit", name, self.debit_account, self.date, self.description, self.debit_amount
        )

        self.update_and_balance_account(self.debit_account, "debit", self.debit_amount)

        name = self.name + "-credit"
        self.create_ledger_entry(
            "credit", name, self.credit_account, self.date, self.description, self.credit_amount
        )

        self.update_and_balance_account(self.credit_account, "credit", self.credit_amount)

    def create_ledger_entry(self, transaction_type, name, account, date, description, amount):
        ledger_entry = frappe.new_doc('Ledger Entry')
        ledger_entry.entry_name = name
        ledger_entry.account = account
        ledger_entry.date = date
        ledger_entry.description = description

        if transaction_type == "debit":
            ledger_entry.debit = amount
        elif transaction_type == "credit":
            ledger_entry.credit = amount
        else:
            frappe.throw("Invalid transaction type.")

        ledger_entry.insert()

    def on_update(self):
        old_journal_entry = self.get_doc_before_save()

        if old_journal_entry is None:
            return

        name = self.name + "-debit"
        self.update_ledger_entry(
            "debit", name, self.debit_account, self.date, self.description, self.debit_amount
        )

        self.update_and_balance_account(
            self.debit_account, "debit", self.debit_amount - old_journal_entry.debit_amount
        )

        name = self.name + "-credit"
        self.update_ledger_entry(
            "credit", name, self.credit_account, self.date, self.description, self.credit_amount
        )

        self.update_and_balance_account(
            self.credit_account, "credit", self.credit_amount - old_journal_entry.credit_amount
        )

    def update_ledger_entry(self, transaction_type, name, account, date, description, amount):
        ledger_entry = frappe.get_doc('Ledger Entry', name)
        ledger_entry.account = account
        ledger_entry.date = date
        ledger_entry.description = description

        if transaction_type == "debit":
            ledger_entry.debit = amount
        elif transaction_type == "credit":
            ledger_entry.credit = amount
        else:
            frappe.throw("Invalid transaction type.")

        ledger_entry.save()

    def update_and_balance_account(self, account_name, transaction_type, amount):
        account = frappe.get_doc('Account', account_name)

        if transaction_type == "debit":
            account.debit += amount
        elif transaction_type == "credit":
            account.credit += amount
        else:
            frappe.throw("Invalid transaction type.")

        if account.debit > account.credit:
            account.balance_amount = account.debit - account.credit
            account.balance_type = 'Debit'
        elif account.credit > account.debit:
            account.balance_amount = account.credit - account.debit
            account.balance_type = 'Credit'
        else:
            account.balance_amount = 0
            account.balance_type = 'None'

        account.save()

        parent = account.get_parent()

        if parent:
            self.update_and_balance_account(parent.name, transaction_type, amount)

    def after_delete(self):
        name = self.name + "-debit"
        frappe.delete_doc('Ledger Entry', name)

        self.update_and_balance_account(self.debit_account, "debit", -self.debit_amount)

        name = self.name + "-credit"
        frappe.delete_doc('Ledger Entry', name)

        self.update_and_balance_account(self.credit_account, "credit", -self.credit_amount)
