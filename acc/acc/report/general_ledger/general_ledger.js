// Copyright (c) 2022, Anand and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
  filters: [
    {
      fieldname: "account",
      label: "Account",
      fieldtype: "Link",
      options: "Account",
    },
  ],
};
