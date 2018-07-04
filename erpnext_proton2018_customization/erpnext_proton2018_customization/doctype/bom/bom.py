# -*- coding: utf-8 -*-
# Copyright (c) 2018, mexarm and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.data import cint
from frappe.model.document import Document
from erpnext.selling.doctype.sales_order.sales_order import get_default_bom_item

def get_exploded_items_from_bom(bom_no):
        exploded_items = frappe.get_all('BOM Explosion Item', filters = { 'parent': bom_no }, fields=['item_code', 'stock_qty'])
        return exploded_items

def get_exploded_items_from_production_order(production_order_id):
        bom_no = frappe.get_value('Production Order', production_order_id, 'bom_no')
        if not bom_no: return []
        return get_exploded_items_from_bom(bom_no)

@frappe.whitelist()
def get_raw_materials_cost_for_item(item_code):
        bom_no = get_default_bom_item(item_code)
        bom = frappe.get_doc("BOM" , bom_no)
        if bom: return bom.raw_material_cost
        item = frappe.get_doc("Item", item_code)
        if item: return item.valuation_rate
        return 0.0

@frappe.whitelist()
def get_raw_materials_cost_and_sla_for_item(item_code):
        bom_no = get_default_bom_item(item_code)
        bom = frappe.get_doc("BOM" , bom_no)
        hora_limite_de_entrega_de_archivos = frappe.db.get_single_value("Proton Setup", "hora_limite_de_entrega_de_archivos")
        if bom: return { 'raw_material_cost': bom.raw_material_cost, 'nivel_de_servicio': bom.nivel_de_servicio, 'hora_limite_de_entrega_de_archivos': hora_limite_de_entrega_de_archivos }
        item = frappe.get_doc("Item", item_code)
        if item: return { 'raw_material_cost': item.valuation_rate, 'nivel_de_servicio': 0, 'hora_limite_de_entrega_de_archivos': hora_limite_de_entrega_de_archivos }
        return { 'raw_material_cost': 0.0, 'nivel_de_servicio': 0, 'hora_limite_de_entrega_de_archivos': hora_limite_de_entrega_de_archivos  }

@frappe.whitelist()
def default_bom_item_has_adicionales_variables(item_code):
        bom_no = get_default_bom_item(item_code)
        if bom_no:
            return frappe.get_value("BOM",bom_no,"adicionales_variables")
        return False
