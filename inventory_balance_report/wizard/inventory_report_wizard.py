from odoo import models, fields
from datetime import timedelta
import io
import base64
try:
    from xlsxwriter import Workbook
except ImportError:
    Workbook = None

class InventoryReportWizard(models.TransientModel):
    _name = 'inventory.report.wizard'
    _description = 'Inventory Report Wizard'

    date_from = fields.Date(string="From", required=True)
    date_to = fields.Date(string="To", required=True)
    location_ids = fields.Many2many('stock.location', string="Locations")
    category_id = fields.Many2one('product.category', string="Product Category")
    product_id = fields.Many2one('product.product', string="Product")

    def _compute_opening_qty(self, product, date_from, location):
        domain = [
            ('product_id', '=', product.id),
            ('move_id.state', '=', 'done'),
            ('date', '<', date_from)
        ]
        domain_in = domain + [('location_dest_id', '=', location.id)]
        domain_out = domain + [('location_id', '=', location.id)]

        in_qty = sum(self.env['stock.move.line'].search(domain_in).mapped('quantity_product_uom'))
        out_qty = sum(self.env['stock.move.line'].search(domain_out).mapped('quantity_product_uom'))

        return in_qty - out_qty

    def action_generate_report(self):
        self.env['inventory.report.line'].search([]).unlink()

        domain = [('is_storable', '=', True)]
        if self.category_id:
            domain.append(('categ_id', '=', self.category_id.id))
        if self.product_id:
            domain.append(('id', '=', self.product_id.id))

        products = self.env['product.product'].search(domain)
        locations = self.location_ids or self.env['stock.location'].search([('usage', '=', 'internal')])

        for product in products:
            for location in locations:
                opening_qty = self._compute_opening_qty(product, self.date_from, location)

                in_qty = sum(self.env['stock.move.line'].search([
                    ('product_id', '=', product.id),
                    ('move_id.state', '=', 'done'),
                    ('location_dest_id', '=', location.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                ]).mapped('quantity_product_uom'))

                out_qty = sum(self.env['stock.move.line'].search([
                    ('product_id', '=', product.id),
                    ('move_id.state', '=', 'done'),
                    ('location_id', '=', location.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                ]).mapped('quantity_product_uom'))

                balance = opening_qty + in_qty - out_qty

                if not any([opening_qty, in_qty, out_qty, balance]):
                    continue

                self.env['inventory.report.line'].create({
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'opening_qty': opening_qty,
                    'in_qty': in_qty,
                    'out_qty': out_qty,
                    'balance': balance,
                    'location_id': location.id,
                })

        if self._context.get('from_report_xlsx_pdf', False):
            return True

        location_names = ", ".join(self.location_ids.mapped('display_name')) if self.location_ids else "All Locations"
        return {
            'type': 'ir.actions.act_window',
            'name': f"Inventory Balance from {self.date_from.strftime('%Y-%m-%d')} to {self.date_to.strftime('%Y-%m-%d')} - {location_names}",
            'res_model': 'inventory.report.line',
            'view_mode': 'list',
            'target': 'current',
        }

    def export_to_excel(self):
        self.with_context(from_report_xlsx_pdf=True).action_generate_report()

        if not Workbook:
            raise ImportError("xlsxwriter library is required for Excel export. Please install it using: pip install xlsxwriter")

        # Create Excel file in memory
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('تقرير رصيد المخزون')

        # Formats
        bold_green = workbook.add_format({
            'bold': True,
            'bg_color': '#28a745',
            'color': 'white',
            'border': 1,
            'align': 'right'
        })
        normal_text = workbook.add_format({
            'border': 1,
            'align': 'right'
        })
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'right',
            'text_wrap': True
        })

        # Report Address
        location_names = ', '.join(self.location_ids.mapped('name')) if self.location_ids else 'All Locations'
        title = f"Inventory Balance Report for Location: {location_names} from Date: {self.date_from.strftime('%Y-%m-%d')} to Date: {self.date_to.strftime('%Y-%m-%d')}"
        sheet.merge_range('A1:G2', title, header_format)

        # Column Size
        sheet.set_column(0, 0, 25)  # Location Column
        sheet.set_column(1, 1, 35)  # Product Column
        sheet.set_column(2, 6, 15)  # Other Columns

        # Column Header
        headers = ['Location', 'Product', 'Unit', 'Opening Quantity', 'Incoming', 'Outgoing', 'Current Balance']

        for col, header in enumerate(headers):
            sheet.write(3, col, header, bold_green)

        # Data
        row = 4
        lines = self.env['inventory.report.line'].search([], order='location_id, product_id')
        for line in lines:
            sheet.write(row, 0, line.location_id.name or '', normal_text)
            sheet.write(row, 1, line.product_id.display_name or '', normal_text)
            sheet.write(row, 2, line.product_uom.name or '', normal_text)
            sheet.write(row, 3, line.opening_qty or 0.0, normal_text)
            sheet.write(row, 4, line.in_qty or 0.0, normal_text)
            sheet.write(row, 5, line.out_qty or 0.0, normal_text)
            sheet.write(row, 6, line.balance or 0.0, normal_text)
            row += 1

        workbook.close()
        output.seek(0)

        # Create attachment
        filename = f'Inventory_Balance_Report_{self.date_to.strftime("%Y-%m-%d")}.xlsx'
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'store_fname': filename,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }

    def export_to_pdf(self):
        self.with_context(from_report_xlsx_pdf=True).action_generate_report()
        report_id = self.env.ref('inventory_balance_report.inventory_report_pdf_action')
        return report_id.report_action(self)
