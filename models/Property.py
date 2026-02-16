from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

class Property(models.Model):
    _name = "estate.property"
    _description = """
    The Property description to llok if can be sold.
    """

    name = fields.Char()
    last_seen = fields.Datetime(
        "Last Seen",
        default=fields.Datetime.now
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=datetime.today() + relativedelta(months=3), 
        copy=False
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    active = fields.Boolean(default=True)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north','North'), ('south', 'South'), ('east', 'East'), ('west', 'West')
        ],
        help="The garden position view."
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new','New'), ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        help="The property's state."
    )

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    bayer_id = fields.Many2one("res.partner", string = "Bayer")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default= lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_is_garden(self):
        if self.garden:
           self.garden_area = 10
           self.garden_orientation = "north"
        else:
           self.garden_area = 0
           self.garden_orientation = None

    def action_cancel_sell(self):
        for record in self:
            if record.state == "sold":
                raise UserError(Exception("The property is selled."))
            else:
                record.state = "cancelled"
        return True
    
    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(Exception("The property is cancelled."))
            else:
                record.state = "sold"
        return True
