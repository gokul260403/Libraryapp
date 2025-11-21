import frappe

def get_context(context):
     

  
    total_members = frappe.db.count("Library Member")

   
    total_books = frappe.db.count("Book")
    total=0
    available=0
    Books = frappe.db.get_all("Book", fields=["total_stock", "available_stocks"])
 
    for book in Books:
        total+=book.total_stock 
        available+=book.available_stocks 
    total_issued=total-available
  

    # total_overdue = frappe.db.count("Library Transaction", {"status": "Overdue"})
 
    context.total_members = total_members
    context.total_books = total_books
    context.total_issued = total_issued
    # context.total_overdue = total_overdue

    return context
