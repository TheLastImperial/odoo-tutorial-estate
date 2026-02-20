from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"
    def action_sold(self):

        # partner_id = self.env['res.partner'].search([('name', '=', 'ClienteCoorporativo')], limit=1).id
        # product_id = self.env['product.product'].search([('name', '=', 'Your Product Name')], limit=1).id
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1) # Get a sales journal
        if not self.selling_price:
            self.selling_price = self.best_price

        invoice_vals = {
            'partner_id': self.bayer_id.id,
            'move_type': 'out_invoice', # Specifies it's a customer invoice
            'date': fields.Date.today(),
            'journal_id': journal.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name,
                    # 'product_id': product_id,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                (0, 0, {
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                }),
                (0, 0, {
                    'name': '6% of the selling price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
            ],
        }

        # Create invoice
        self.env['account.move'].create(invoice_vals)

        return super().action_sold()

