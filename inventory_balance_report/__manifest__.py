{
    "name": "Inventory Balance Report",
    "version": "17.0.0.1",
    "summary": "This module provides a comprehensive Inventory Balance Report that allows users to view stock levels as of a specific date. It calculates and displays"
               "Opening Balance before the selected date"
               "Total Incoming Quantity within the selected period"
               "Total Outgoing Quantity within the selected period"
               "Current Balance up to the specified date",
    "description": """
        Inventory Balance Report
        This module provides comprehensive inventory balance reporting functionality for tracking
        stock movements and current inventory levels across your warehouse.
        Key Features:
        * Generate inventory reports by specific date ranges
        * View opening balance for products at the start of the reporting period
        * Track incoming quantities (receipts, returns, adjustments)
        * Track outgoing quantities (deliveries, consumption, adjustments)
        * Calculate current/closing balance automatically
        * Filter reports by product, category, location, or warehouse
        * Export reports in multiple formats (PDF and Excel)
        * User-friendly wizard interface for report generation
        * Detailed product-wise inventory movement analysis
        Use Cases:
        * Period-end inventory reconciliation
        * Stock audit and verification
        * Inventory valuation reports
        * Movement analysis for specific products or locations
        * Historical inventory tracking and analysis
        The module seamlessly integrates with Odoo's stock management system and provides
        accurate, real-time inventory data for better decision making.
    """,
    "category": "Inventory",
    "author": "ModSaeed",
    "depends": ["stock", "base"],
    "data": [
        "security/ir.model.access.csv",
        "report/inventory_balance_report_pdf.xml",
        "report/inventory_balance_template.xml",
        "views/inventory_report_action_menu.xml",
        "views/inventory_report_views.xml",
        "wizard/inventory_report_wizard_views.xml",
    ],
    'external_dependencies': {
        'python': ['xlsxwriter'],
    },
    'images': ['static/description/images/images.png','static/description/images/images.png'],
    "license": "OPL-1",
    "currency": "EUR",
    "price": 64.0,
    "installable": True,
    "application": True
}
