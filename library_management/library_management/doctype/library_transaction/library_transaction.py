# Copyright (c) 2025, demo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import today

class LibraryTransaction(Document):
	def before_save(self):
		self.date_of_transaction = today()
  
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			article = frappe.get_doc("Book", self.book)
			# article.status = "Issued"
			article.available_stocks -= 1
			article.save()

		elif self.type == "Return":
			self.validate_return()
			article = frappe.get_doc("Book", self.book)
			# article.status = "Available"
			article.available_stocks += 1
			article.save()

	def validate_issue(self):
		self.validate_membership()
		article=frappe.get_doc("Book",self.book)
		if article.available_stocks==0:
			frappe.throw("No Books available")
		
	# def validate_return(self):
	# 	self.validate_membership()
	# 	article=frappe.get_doc("Book",self.book)
	# 	if article.status =="Available":
	# 		frappe.throw("Return Invalid")
   
   
	# def validate_return(self):
	# 	self.validate_membership()
	# 	issued_record = frappe.db.exists(
	# 		"Library Transaction",
	# 		{
	# 			"library_member": self.library_member,
	# 			"book": self.book,
	# 			"type": "Issue",
	# 			"docstatus": 1,   
	# 		},
	# 	)
	# 	if not issued_record:
	# 		frappe.throw(
	# 			f"This book was not issued to {self.library_member}. "
	# 			"You cannot return it."
	# 		)

	# 	article = frappe.get_doc("Book", self.book)
	# 	if article.status == "Available":
	# 		frappe.throw("Invalid return — this book is already available.")
   
	def validate_return(self):
		self.validate_membership()

		issued_count = frappe.db.count(
			"Library Transaction",
			{
				"library_member": self.library_member,
				"book": self.book,
				"type": "Issue",
				"docstatus": 1,
			},
		)


		returned_count = frappe.db.count(
			"Library Transaction",
			{
				"library_member": self.library_member,
				"book": self.book,
				"type": "Return",
				"docstatus": 1,
			},
		)

		if returned_count >= issued_count:
			frappe.throw(
				f"No outstanding issued books found for {self.library_member} to return."
			)
	def validate_membership(self):
		print("library_member:", self.library_member)
		
		membership = frappe.db.exists("Library Membership", {
			"name1": self.library_member,
			"docstatus": 1,  
			"from_date": ("<=", self.date_of_transaction),
			"to_date": (">=", self.date_of_transaction)
		})
	 
		
		if not membership:
			frappe.throw("You do not have a valid membership for this date.")

    
	def after_insert(self):
		if self.docstatus == 0:
			self.submit()