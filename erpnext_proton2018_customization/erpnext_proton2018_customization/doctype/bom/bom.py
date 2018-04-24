# -*- coding: utf-8 -*-
# Copyright (c) 2018, mexarm and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.data import cint
from frappe.model.document import Document

def get_exploded_items_from_bom(bom_no):
        exploded_items = frappe.get_all('BOM Explosion Item', filters = { 'parent': bom_no }, fields=['item_code', 'stock_qty'])
        return exploded_items

def get_exploded_items_from_production_order(production_order_id):
        bom_no = frappe.get_value('Production Order', production_order_id, 'bom_no')
        if not bom_no: return []
        return get_exploded_items_from_bom(bom_no)
