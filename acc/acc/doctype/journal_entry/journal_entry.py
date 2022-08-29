# Copyright (c) 2022, Anand and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from acc.acc.utils import create_ledger_entry


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
        create_ledger_entry(
            "debit", name, self.debit_account, self.datetime, self.description, self.debit_amount
        )

        name = self.name + "-credit"
        create_ledger_entry(
            "credit", name, self.credit_account, self.datetime, self.description, self.credit_amount
        )

    def on_cancel(self):
        name = self.name + "-cancel-debit"
        create_ledger_entry(
            "debit", name, self.credit_account, self.datetime, self.description, self.credit_amount
        )

        name = self.name + "-cancel-credit"
        create_ledger_entry(
            "credit", name, self.debit_account, self.datetime, self.description, self.debit_amount
        )
