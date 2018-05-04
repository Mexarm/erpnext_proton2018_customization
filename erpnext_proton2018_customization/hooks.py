# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "erpnext_proton2018_customization"
app_title = "Erpnext Proton2018 Customization"
app_publisher = "mexarm"
app_description = "Customization for Proton Logistics (2018)"
app_icon = "far fa-edit"
app_color = "grey"
app_email = "armando.hernandez@protonmexico.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpnext_proton2018_customization/css/erpnext_proton2018_customization.css"
# app_include_js = "/assets/erpnext_proton2018_customization/js/erpnext_proton2018_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpnext_proton2018_customization/css/erpnext_proton2018_customization.css"
# web_include_js = "/assets/erpnext_proton2018_customization/js/erpnext_proton2018_customization.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "erpnext_proton2018_customization.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "erpnext_proton2018_customization.install.before_install"
# after_install = "erpnext_proton2018_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpnext_proton2018_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"erpnext_proton2018_customization.tasks.all"
# 	],
# 	"daily": [
# 		"erpnext_proton2018_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"erpnext_proton2018_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"erpnext_proton2018_customization.tasks.weekly"
# 	]
# 	"monthly": [
# 		"erpnext_proton2018_customization.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "erpnext_proton2018_customization.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpnext_proton2018_customization.event.get_events"
# }
fixtures = ["Custom Field", "Custom Script", "Property Setter", "Print Format",
            {"dt" : "DocType", "filters": [["name", "in", ("Grafica de Impresion","Spool Entry")]]},
            {"dt": "Workflow State", "filters": [["name", "in", ("Borrador","Liberado", "Imprimiendose", "Finalizado", "Rechazado")]] },
            {"dt": "Workflow Action", "filters": [["name", "in", ("Liberar","Imprimir", "Finalizar", "Rechazar")]]},
            "Workflow" ]
