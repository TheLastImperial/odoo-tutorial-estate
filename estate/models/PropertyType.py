from odoo import _, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = """
        Types of properties.
    """
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id"
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )
    _order = "name"


    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_related_offers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'list',
            'res_model': 'estate.property.offer',
            'domain': [('id', 'in', self.offer_ids.mapped("id"))],
            'context': "{'create': False}"
        }
