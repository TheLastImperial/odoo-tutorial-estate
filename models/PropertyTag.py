from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = """
        Tags for properties
    """
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The tag name must be unique."
    )
