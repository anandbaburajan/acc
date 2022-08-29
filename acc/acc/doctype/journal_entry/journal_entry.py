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

    def on_submit(self):
        name = self.name + "-debit"
        self.create_ledger_entry(
            "debit", name, self.debit_account, self.datetime, self.description, self.debit_amount
        )

        name = self.name + "-credit"
        self.create_ledger_entry(
            "credit", name, self.credit_account, self.datetime, self.description, self.credit_amount
        )

    def on_cancel(self):
        name = self.name + "-cancel-debit"
        self.create_ledger_entry(
            "debit", name, self.credit_account, self.datetime, self.description, self.credit_amount
        )

        name = self.name + "-cancel-credit"
        self.create_ledger_entry(
            "credit", name, self.debit_account, self.datetime, self.description, self.debit_amount
        )

    def create_ledger_entry(self, transaction_type, name, account, datetime, description, amount):
        ledger_entry = frappe.new_doc('General Ledger')
        ledger_entry.entry_name = name
        ledger_entry.account = account
        ledger_entry.datetime = datetime
        ledger_entry.description = description

        if transaction_type == "debit":
            ledger_entry.debit = amount
        elif transaction_type == "credit":
            ledger_entry.credit = amount
        else:
            frappe.throw("Invalid transaction type.")

        ledger_entry.insert()
