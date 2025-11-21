frappe.pages['dashboard-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});

	  page.add_action_icon("refresh", () => {
        frappe.msgprint("Page refreshed!");
    });
    const $content = $(`
        <div class="dashboard-wrapper" style="padding: 20px;">
            <div class="row">
                <div class="col-sm-4">
                    <div class="card shadow-sm  bg-light text-center p-3">
                        <h4>Total Books</h4>
                        <h2 id="total_books">--</h2>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="card shadow-sm text-center p-3">
                        <h4>Total Members</h4>
                        <h2 id="total_sales">--</h2>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="card shadow-sm  bg-light text-center p-3">
                        <h4>Pending Returns</h4>
                        <h2 id="pending_Returns">--</h2>
                    </div>
                </div>
            </div>
        </div>
    `);

    $content.appendTo(page.body);



}