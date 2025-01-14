from odoo import models, fields, api
from collections import defaultdict

class InventoryNetBalanceReport(models.TransientModel):
    _name = 'inventory.net.balance.report'
    _description = 'Inventory Net Balance Report'
    
    product_ids = fields.Many2many('product.product', string='Products')
    location_ids = fields.Many2many('stock.location', string='Locations')
    location_usage = fields.Selection(
        related='location_ids.usage',
        string="Location Type",
        readonly=False
    )
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", default=fields.Date.today())
    report_lines = fields.One2many('inventory.net.balance.report.line', 'report_id', string="Report Lines")

    @api.onchange('location_usage')
    def _onchange_location_usage(self):
        if self.location_usage:
            domain = [('usage', '=', self.location_usage)]
            locations = self.env['stock.location'].search(domain)
            self.location_ids = locations
        else:
            self.location_ids = False

    def generate_report(self):
        self.ensure_one()
        lines = []
        domain = []

        if self.location_ids:
            domain.append(('location_id', 'in', self.location_ids.ids))
        if self.location_usage:
            domain.append(('location_id.usage','=', self.location_usage))
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))

        if self.date_from and self.date_to:
            domain.append(('create_date','>=',self.date_from))
            domain.append(('create_date','<=',self.date_to))

        quants = self.env['stock.quant'].search(domain)
        
        grouped_data = defaultdict(lambda: defaultdict(lambda: {
            'quantity': 0.0,
            'available_quantity': 0.0,
            'reserved_quantity': 0.0,
            'uom_name':''
        }))
        for quant in quants:
            product_key = (quant.product_id.id, quant.product_id.name, quant.product_id.default_code, quant.product_id.uom_id.name)
            location_key = (quant.location_id.id, quant.location_id.name)
            
            grouped_data[product_key][location_key]['quantity'] += quant.quantity
            grouped_data[product_key][location_key]['available_quantity'] += quant.available_quantity
            grouped_data[product_key][location_key]['reserved_quantity'] += quant.reserved_quantity
            grouped_data[product_key][location_key]['uom_name'] = quant.product_id.uom_id.name
        for (product_id, product_name, product_code, uom_name), location_data in grouped_data.items():
            for (location_id, location_name), values in location_data.items():
                lines.append((0, 0, {
                    'product_name': product_name,
                    'product_code': product_code,
                    'location_name': location_name,
                    'quantity': values['quantity'],
                    'available_quantity': values['available_quantity'],
                    'reserved_quantity': values['reserved_quantity'],
                    'uom_name': uom_name,
                }))
        
        self.report_lines = [(5, 0, 0)] + lines

        return {
            'name': 'Inventory Net Balance Report',
            'type': 'ir.actions.act_window',
            'res_model': 'inventory.net.balance.report',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'main',
        }

    def print_report(self):
        self.ensure_one()
        return self.env.ref('inventory_reports.action_inventory_net_balance_report').report_action(self, data=None)
    


class InventoryNetBalanceReportLine(models.TransientModel):
    _name = 'inventory.net.balance.report.line'
    _description = 'Inventory Net Balance Report Line'

    report_id = fields.Many2one('inventory.net.balance.report', string="Report")

    product_name = fields.Char(string="Product Name")
    product_code = fields.Char(string="Product Code")
    location_name = fields.Char(string="Location")
    quantity = fields.Float(string="On Hand Quantity")
    available_quantity = fields.Float(string="Available Quantity")
    reserved_quantity = fields.Float(string="Reserved Quantity")
    uom_name = fields.Char(string="Unit of Measure")