# -*- coding: utf-8 -*-
# Copyright (c) 2018, mexarm and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.utils.data import cint, flt
from frappe.model.document import Document
from erpnext_proton2018_customization.erpnext_proton2018_customization.doctype.bom.bom import get_exploded_items_from_production_order

#class StockEntry(Document):
#	pass
def get_print_process_required(item_name):
        return cint(frappe.get_value('Item', item_name, 'print_process_required'))

def add_qty(store_dict, k, v):
        if k in store_dict:
                store_dict[k] += v
        else:
                store_dict[k] = v

@frappe.whitelist()
def get_stock_entry_items_to_transfer(production_order_id, wip_impresion, wip_produccion):
        '''returns stock items that need to be transferred from wip impresion to wip produccion'''
        items = []
        po = frappe.get_doc('Production Order', production_order_id)
        ste_list = frappe.get_all('Stock Entry', filters={'production_order': production_order_id, 
                                                          'purpose': 'Material Transfer for Manufacture',
                                                           'docstatus': 1 }, 
                                   fields=['name']) 
        en_impresion = {}
        en_produccion = {}
        for ste in ste_list:
                items = frappe.get_all('Stock Entry Detail', filters={'parent': ste.name }, fields = ['item_code', 'qty', 'transfer_qty', 
                                                                                                      's_warehouse', 't_warehouse'])
                for item in items:
                        wip_p = (item.s_warehouse == wip_impresion) and (item.t_warehouse == wip_produccion)
                        wip_i = item.t_warehouse == wip_impresion
                        if wip_p:
                                add_qty(en_produccion, item.item_code, item.qty)
                        if wip_i:
                                add_qty(en_impresion, item.item_code, item.qty)
        for key in en_impresion:
                en_impresion[key] -= en_produccion.get(key,0)
        return en_impresion

@frappe.whitelist()
def get_transferred_qty(production_order_id, item_list):
        """get the minumum qty that can be manufactured with the transferred item_list"""
        exploded_items = get_exploded_items_from_production_order(production_order_id)
        exploded_items_dict = { i['item_code']:i['stock_qty'] for i in exploded_items }
        item_list = json.loads(item_list)
        qty = []
        for item in item_list:
                item_qty = (flt(item['qty'])) / flt(exploded_items_dict[item['item_code']])  
                if not item_qty.is_integer():
                        frappe.throw(_("item {0} has not valid qty, qty should be divisible by {1}  ").format(item.item_code, exploded_items_dict[item.item_code]))
                qty.append(item_qty)
        return min(qty)

@frappe.whitelist()
def get_proton_setup_settings():
        """returns the Proton Setup Settings"""
        return { "almacen_wip_impresion":  frappe.db.get_single_value('Proton Setup', 'almacen_wip_impresion'),
                 "almacen_wip_produccion": frappe.db.get_single_value('Proton Setup', 'almacen_wip_produccion'),
                 "hora_limite_de_entrega_de_archivos": frappe.db.get_single_value('Proton Setup', 'hora_limite_de_entrega_de_archivos')}

@frappe.whitelist()
def  check_SO_adicionales_variables(production_order_name):
        """Check if the parent sales order of the  production order has an associated Sales Order for the additional items, if so returns true, else returns false"""
        po = frappe.get_doc("Production Order",  production_order_name)
        if po.sales_order:
                so = frappe.get_doc("Sales Order", po.sales_order)
                if so.adicionales_variables:
                        if so.orden_de_venta_de_los_adicionales:
                                so_adicionales = frappe.get_doc("Sales Order", so.orden_de_venta_de_los_adicionales)
                                if so_adicionales.docstatus == 1:
                                        return { "validated" : True, "message": "validated" }
                                else:
                                        return { "validated": False, "message": "La Orden de Venta {} de adicionales variables existe pero no se ha validado (not submitted)".format(so.orden_de_venta_de_los_adicionales) }
                        else:
                                return { "validated": False, "message": "se requiere un Orden de Venta para los adicionales, pero esta no se ha indicado en la OV principal {}".format(po.sales_order) }# se requiere una OV para los adicionales pero no se ha encontrado
                else:
                        return { "validated": True, "message": "no se requieren adicionales"} # no se requieren adicionales
        else:
                return { "validated": False, "message": "Error no se Encuentra Orden de Venta para la Orden de Produccion {}".format(production_order_name) }  #error al leer la  orden de  Produccion
