// Copyright (c) 2022, Anand and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice", {
  update_item_amount: function (cdt, cdn) {
    let row = locals[cdt][cdn];
    const amount = row.quantity * row.rate;
    frappe.model.set_value(cdt, cdn, "amount", amount);
  },
  update_net_and_total: function (frm) {
    let amount = 0;
    $.each(frm.doc.items || [], function (i, item) {
      amount += item.amount;
    });

    frm.set_value("net", amount);
    frm.set_value("total", amount + frm.doc.vat);
  },
  vat(frm, cdt, cdn) {
    frm.set_value("total", frm.doc.net + frm.doc.vat);
  },
});

frappe.ui.form.on("Item", {
  quantity(frm, cdt, cdn) {
    frm.events.update_item_amount(cdt, cdn);
    frm.events.update_net_and_total(frm);
  },
  rate(frm, cdt, cdn) {
    frm.events.update_item_amount(cdt, cdn);
    frm.events.update_net_and_total(frm);
  },
  items_remove(frm, cdt, cdn) {
    frm.events.update_net_and_total(frm);
  },
});
