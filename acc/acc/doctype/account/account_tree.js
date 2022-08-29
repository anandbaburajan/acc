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
    let accounts = [];
    if (deep) {
      // in case of `get_all_nodes`
      accounts = nodes.reduce((acc, node) => [...acc, ...node.data], []);
    } else {
      accounts = nodes;
    }

    const get_balances = frappe.call({
      method: "acc.acc.utils.get_account_balances",
      args: {
        accounts: accounts,
      },
    });

    get_balances.then((r) => {
      for (let account of r.message) {
        const node = cur_tree.nodes && cur_tree.nodes[account.value];
        if (!node || node.is_root) continue;

        const balance = account.balance;
        const balance_type = balance > 0 ? "Dr" : "Cr";

        node.parent && node.parent.find(".balance-area").remove();
        $(
          '<span class="balance-area pull-right">' +
            Math.abs(balance) +
            " " +
            balance_type +
            "</span>"
        ).insertBefore(node.$ul);
      }
    });
  },
};
