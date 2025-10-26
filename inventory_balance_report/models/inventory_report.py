from odoo import models, fields

class InventoryReportLine(models.TransientModel):
    _name = 'inventory.report.line'
    _description = 'Inventory Report Line'

    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    product_uom = fields.Many2one('uom.uom', string="Unit", readonly=True)
    location_id = fields.Many2one('stock.location', string="Location", readonly=True)
    opening_qty = fields.Float(string="Opening Quantity", readonly=True)
    in_qty = fields.Float(string="Incoming", readonly=True)
    out_qty = fields.Float(string="Outgoing", readonly=True)
    balance = fields.Float(string="Current Balance", readonly=True)


class InventoryBalanceReportPDF(models.AbstractModel):
    _name = 'report.inventory_balance_report.inventory_report_pdf'
    _description = 'Inventory Balance Report PDF'

    def _get_report_values(self, docids, data=None):
        docs = self.env['inventory.report.wizard'].browse(docids)
        report_lines = self.env['inventory.report.line'].search([], order='location_id, product_id')
        return {
            'doc_ids': docids,
            'doc_model': 'inventory.report.wizard',
            'docs': docs,
            'report_lines': report_lines,
        }