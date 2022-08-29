import frappe
import json


@frappe.whitelist()
def get_account_balances(accounts):
    accounts = json.loads(accounts)

    for account in accounts:
        amounts = {}

        if account['expandable']:
            amounts = get_group_account_amounts(account['value'])
        else:
            amounts = get_single_account_amounts(account['value'])

        account['balance'] = amounts['total_debit'] - amounts['total_credit']

    return accounts


def get_single_account_amounts(account):
    amounts = frappe.db.get_list(
        'General Ledger',
        filters={'account': account},
        fields=['sum(debit) as total_debit', 'sum(credit) as total_credit']
    )[0]

    total_debit = amounts['total_debit'] if amounts['total_debit'] else 0
    total_credit = amounts['total_credit'] if amounts['total_credit'] else 0

    return {'total_debit': total_debit, 'total_credit': total_credit}


def get_group_account_amounts(account):
    child_accounts = frappe.db.get_list(
        'Account',
        filters={'parent_account': account},
        fields=['account_name', 'is_group']
    )

    total_debit = 0
    total_credit = 0

    for account in child_accounts:
        if account['is_group']:
            amounts = get_group_account_amounts(account['account_name'])
            total_debit += amounts['total_debit']
            total_credit += amounts['total_credit']
        else:
            amounts = get_single_account_amounts(account['account_name'])
            total_debit += amounts['total_debit']
            total_credit += amounts['total_credit']

    return {'total_debit': total_debit, 'total_credit': total_credit}
