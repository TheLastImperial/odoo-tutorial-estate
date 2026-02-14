from odoo import fields, models
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
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
