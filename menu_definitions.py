from Menu import Menu
from Option import Option

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(sess)"),
    Option("Delete", "delete(sess)"),
    Option("Update", "update(sess)"),
    Option("List", "list_objects(sess)"),
    Option("Reports", "reports(sess)"),
    Option("Boilerplate Data", "boilerplate(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Rollback", "session_rollback(sess)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Vendor", "add_vendor(sess)"),
    Option("Assembly", "add_assembly(sess)"),
    Option("Piece Part", "add_piece_part(sess)"),
    Option("Component to Assembly", "add_component(sess)"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete:', [
    Option("Vendor", "delete_vendor(sess)"),
    Option("Part", "delete_part(sess)"),
    Option("Component from Assembly", "delete_component(sess)"),
    Option("Exit", "pass")
])

update_menu = Menu('update', 'Please indicate what you want to update:', [
    Option("Part Name", "update_part(sess)"),
    Option("Composition Quantity", "update_composition(sess)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Parts", "list_parts(sess)"),
    Option("Vendors", "list_vendors(sess)"),
    Option("Compositions", "list_compositions(sess)"),
    Option("Report a Vendor", "report_vendor(sess)"),
    Option("Report a Part", "report_part(sess)"),
    Option("Report a Composition", "report_composition(sess)"),
    Option("Exit", "pass")
])

report_menu = Menu('reports', 'Please select a report:', [
    Option("Hierarchy Report", "hierarchy_report(sess)"),
    Option("Max Components Report", "max_components_report(sess)"),
    Option("Exit", "pass")
])

debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
