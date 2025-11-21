# Copyright (c) 2025, demo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import today


class LibraryMembership(Document):

	def before_submit(self):
		exists=frappe.db.exists("Library Membership",{
			"name1":self.name1,
			"docstatus":DocStatus.submitted(),
			"to_date" :(">" ,self.from_date),
		},
        )
		if exists:
			frappe.throw("Already you have a Memership")

	def validate(self):
		current_date=today()
		if self.from_date < current_date:
			frappe.throw("Invalid Date: The 'From Date' cannot be in the past.")
		elif self.to_date < self.from_date :
			frappe.throw("Invalid Date: The 'To Date' cannot be before 'From Date'.")
        
	def after_insert(self):
		if self.docstatus == 0:
			self.submit()