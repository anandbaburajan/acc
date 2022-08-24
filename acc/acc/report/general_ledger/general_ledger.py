# Copyright (c) 2022, Anand and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    if not filters:
        return [], []

    columns = [
        {
            'fieldname': 'account',
            'label': 'Account',
            'fieldtype': 'Link',
            'options': 'Account'
        },
        {
            "fieldname": "date",
            "fieldtype": "Date",
            "label": "Date",
        },
        {
            "fieldname": "description",
            "fieldtype": "Data",
            "label": "Description",
        },
        {
            "fieldname": "debit",
            "fieldtype": "Currency",
            "label": "Debit"
        },
        {
            "fieldname": "credit",
            "fieldtype": "Currency",
            "label": "Credit"
        }
    ]

    data = frappe.db.get_list(
        'Ledger Entry',
        filters={'account': filters.get("account")},
        fields=['account', 'date', 'description', 'debit', 'credit'],
        order_by='date desc'
    )

    return columns, data
