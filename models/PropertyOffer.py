from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = """
        Offer for a property.
    """
    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"), ("refused", "Refused")
        ]
    )
    partner_id = fields.Many2one("res.partner",
        string="Partner",
        required=True
    )
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(
        compute="_compute_validity_date",
        inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_validity_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = datetime.today() + relativedelta(days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - datetime.now().date()).days
