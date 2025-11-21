# Copyright (c) 2025, demo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Book(Document):
	def before_insert(self):
		self.available_stocks=self.total_stock
	def validate(self):
		if self.isbn:
			exists = frappe.db.exists({
				"doctype": "Book",
				"isbn": self.isbn,
				"name": ["!=", self.name]   
			})
			if exists:
				frappe.throw(f"ISBN {self.isbn} already exists for another book.") 
			
	def before_save(self):
		total_stock_changed = self.has_value_changed("total_stock")
		if total_stock_changed:
			old_doc = self.get_doc_before_save() or 0
			if old_doc:
				available_stocks = self.total_stock - old_doc.total_stock
				self.available_stocks=self.available_stocks + available_stocks
		 
		
	
				
