{
    "name": "Inventory Balance Report",
    "version": "18.0.0.1",
    "summary": "Advanced Inventory Balance Report/Inventory Report with Opening, Incoming, Outgoing & Current Stock",
    "description": """
        Inventory Balance Report - Complete Stock Movement Tracking
        ===========================================================

        This module provides comprehensive inventory balance reporting functionality for tracking
        stock movements and current inventory levels across your warehouse.

        Key Features:
        -------------
        * Generate inventory reports by specific date ranges
        * View opening balance for products at the start of the reporting period
        * Track incoming quantities (receipts, returns, adjustments)
        * Track outgoing quantities (deliveries, consumption, adjustments)
        * Calculate current/closing balance automatically
        * Filter reports by product, category, location, or warehouse
        * Export reports in multiple formats (PDF and Excel)
        * User-friendly wizard interface for report generation
        * Detailed product-wise inventory movement analysis
        * Real-time stock valuation and tracking

        Use Cases:
        ----------
        * Period-end inventory reconciliation
        * Stock audit and verification
        * Inventory valuation reports
        * Movement analysis for specific products or locations
        * Historical inventory tracking and analysis
        * Warehouse management and stock control
        * Financial reporting and stock audits

        Perfect For:
        ------------
        * Warehouse managers
        * Inventory controllers
        * Stock auditors
        * Accountants needing inventory valuation
        * Operations managers

        The module seamlessly integrates with Odoo's stock management system and provides
        accurate, real-time inventory data for better decision making.

        Keywords: inventory report, stock balance, warehouse report, inventory tracking,
        stock movement, inventory valuation, stock audit, opening balance, closing balance,
        inventory reconciliation, stock analysis, warehouse management
    """,

    "category": "Inventory",
    "author": "ModSaeed",
    "website": "",
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

    # FIXED: Correct path for the icon/thumbnail
    'images': ['static/description/icon.png'],

    "license": "OPL-1",
    "currency": "EUR",
    "price": 55.0,
    "installable": True,
    "application": True,
}