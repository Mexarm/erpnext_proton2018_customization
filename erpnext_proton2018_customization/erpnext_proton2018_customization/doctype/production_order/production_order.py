import frappe
from frappe import _
from frappe.utils import flt
from erpnext.stock.doctype.stock_entry.stock_entry import get_additional_costs

class StockOverProductionError(frappe.ValidationError): pass

def update_production_order_qty(self):
                """Update **Manufactured Qty** and **Material Transferred for Qty** in Production Order
                        based on Stock Entry"""
                for purpose, fieldname in (("Manufacture", "produced_qty"),):
                        qty = flt(frappe.db.sql("""select sum(fg_completed_qty)
                                from `tabStock Entry` where production_order=%s and docstatus=1
                                and purpose=%s""", (self.name, purpose))[0][0])
                        if qty > (self.qty):
                                frappe.throw(_("{0} ({1}) cannot be greater than planned quantity ({2}) in Production Order {3}").format(\
                                        self.meta.get_label(fieldname), qty, self.qty, self.name), StockOverProductionError)

                        self.db_set(fieldname, qty)

                transfer_qty = []
                for purpose, fieldname, tipo in (("Material Transfer for Manufacture", "material_transferred_for_manufacturing_impresion", "impresion"),
                        ("Material Transfer for Manufacture", "material_transferred_for_manufacturing_produccion", "produccion")):
                        qty = flt(frappe.db.sql("""select sum(fg_completed_qty)
                                from `tabStock Entry` where production_order=%s and docstatus=1
                                and purpose=%s and tipo=%s""", (self.name, purpose, tipo))[0][0])
                        if 'material_transferred_for_manufacturing_' in fieldname:
                                transfer_qty.append(qty)
                        if qty > (self.qty):
                                frappe.throw(_("{0} ({1}) cannot be greater than planned quantity ({2}) in Production Order {3}").format(\
                                        self.meta.get_label(fieldname), qty, self.qty, self.name), StockOverProductionError)

                        self.db_set(fieldname, qty)
                self.db_set('material_transferred_for_manufacturing', min(transfer_qty))

@frappe.whitelist()
def make_stock_entry(production_order_id, purpose, qty=None, tipo=None):
        production_order = frappe.get_doc("Production Order", production_order_id)
        if not frappe.db.get_value("Warehouse", production_order.wip_warehouse, "is_group") \
                        and not production_order.skip_transfer:
                wip_warehouse = production_order.wip_warehouse
        else:
                wip_warehouse = None

        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.purpose = purpose
        stock_entry.production_order = production_order_id
        stock_entry.company = production_order.company
        stock_entry.from_bom = 1
        stock_entry.bom_no = production_order.bom_no
        stock_entry.use_multi_level_bom = production_order.use_multi_level_bom
        stock_entry.fg_completed_qty = qty or (flt(production_order.qty) - flt(production_order.produced_qty))

        if purpose=="Material Transfer for Manufacture":
                stock_entry.to_warehouse = wip_warehouse
                stock_entry.project = production_order.project
        else:
                stock_entry.from_warehouse = wip_warehouse
                stock_entry.to_warehouse = production_order.fg_warehouse
                additional_costs = get_additional_costs(production_order, fg_qty=stock_entry.fg_completed_qty)
                stock_entry.project = production_order.project
                stock_entry.set("additional_costs", additional_costs)

        stock_entry.get_items()
        # customization
        stock_entry.tipo = tipo
	items = []
        value = 1 if tipo == 'impresion' else 0 
        for i in stock_entry.items:
                print i
                if frappe.get_value('Item', i.item_code, 'print_process_required') == value:
                        items.append(i)
        stock_entry.set('items', items)
        stock_entry.save()
        #
        return stock_entry.as_dict()

#def customize_onload(self):
#	self.update_production_order_qty = update_production_order_qty
