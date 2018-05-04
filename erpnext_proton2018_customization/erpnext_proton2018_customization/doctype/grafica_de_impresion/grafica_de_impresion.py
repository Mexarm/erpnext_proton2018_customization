# -*- coding: utf-8 -*-
# Copyright (c) 2018, mexarm and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class GraficadeImpresion(Document):                                                
                                                                                   
        def validate(self):                                                        
                total=0                                                            
                for spool_entry in self.archivos_spool:                            
                        total += spool_entry.cantidad_de_registros                 
                self.total=total                                                   
#                if (not self.priority) and self.project:                           
#                        self.priority=frappe.db.get_value("Project",self.project,"priority")
@frappe.whitelist()
def save_causa_de_rechazo(form_dict):
        import json
        doc = json.loads(form_dict) 
        if not doc.get('causa_de_rechazo', None):
                frappe.throw("Motivo de Rechazo no especificado")
        if len(doc.get('causa_de_rechazo')) <2:
                frappe.throw("Motivo de Rechazo debe ser de una longitud mayor")
        #gi = frappe.get_doc('Grafica de Impresion',doc.get('name'))
        #if not gi:
        #        frappe.throw("Grafica no encontrada")
        #gi.causa_de_rechazo = doc.get('causa_de_rechazo')
        #return gi.save()
        return frappe.db.set_value('Grafica de Impresion', doc['name'], 'causa_de_rechazo', doc['causa_de_rechazo'])

