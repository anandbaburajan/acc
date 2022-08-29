# Copyright (c) 2022, Anand and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from acc.acc.utils import create_ledger_entry


class Invoice(Document):
    def on_submit(self):
        name = self.name + "-debit"
        create_ledger_entry(
            "debit", name, "Debtors", self.datetime, self.description, self.total
        )

        name = self.name + "-credit"
        create_ledger_entry(
            "credit", name, "Sales", self.datetime, self.description, self.total
        )

    def on_cancel(self):
        name = self.name + "-cancel-debit"
        create_ledger_entry(
            "debit", name, "Sales", self.datetime, self.description, self.total
        )

        name = self.name + "-cancel-credit"
        create_ledger_entry(
            "credit", name, "Debtors", self.datetime, self.description, self.total
        )
