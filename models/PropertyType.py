from odoo import fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = """
        Types of properties.
    """
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
