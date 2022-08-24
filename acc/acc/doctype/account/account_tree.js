// Copyright (c) 2022, Anand and contributors
// For license information, please see license.txt

frappe.treeview_settings["Account"] = {
  breadcrumb: "Acc",
  title: "Chart of Accounts",
  // enable custom buttons beside each node
  extend_toolbar: true,
  // custom buttons to be displayed beside each node
  toolbar: [
    {
      label: __("View Ledger"),
      click: function (node, btn) {
        frappe.route_options = {
          account: node.label,
        };
        frappe.set_route("query-report", "General Ledger");
      },
      btnClass: "hidden-xs",
    },
  ],
  on_get_node: function (nodes, deep = false) {
    const get_balances = frappe.db.get_list("Account", {
      fields: ["account_name", "balance_amount", "balance_type"],
    });
    get_balances.then((r) => {
      for (let account of r) {
        const node = cur_tree.nodes && cur_tree.nodes[account.account_name];
        if (!node || node.is_root) continue;

        const balance = account.balance_amount;
        const balance_type = account.balance_type;

        node.parent && node.parent.find(".balance-area").remove();
        $(
          '<span class="balance-area pull-right">' +
            balance +
            " " +
            balance_type +
            "</span>"
        ).insertBefore(node.$ul);
      }
    });
  },
};
