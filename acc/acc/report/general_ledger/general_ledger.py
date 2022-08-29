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

    data = get_account_data(filters.get("account"))

    return columns, data


def get_account_data(account_name):
    account = frappe.db.get_list(
        'Account',
        filters={'account_name': account_name},
        fields=['account_name', 'is_group'],
    )[0]

    data = []

    if account['is_group']:
        child_accounts = frappe.db.get_list(
            'Account',
            filters={'parent_account': account_name},
            fields=['account_name']
        )

        for child_account in child_accounts:
            data.append(get_account_data(child_account['account_name'])[0])
    else:
        data = frappe.db.get_list(
            'General Ledger',
            filters={'account': account_name},
            fields=['account', 'date', 'description', 'debit', 'credit'],
            order_by='date desc'
        )

    return data
