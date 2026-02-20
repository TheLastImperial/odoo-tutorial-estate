from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

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
        ],
        readonly=True
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
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )

    _order = "price desc"
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The price must be positive."
    )
    @api.model
    def create(self, vals_list):
        record = vals_list[0]
        property_id = vals_list[0]["property_id"]
        offers = self.env["estate.property.offer"].search(
            [('property_id', '=', property_id)]
        )
        if offers:
            prices = offers.mapped("price")
            best_price = max(prices)
            if record["price"] < best_price:
                raise ValidationError(
                    Exception("You most set a better offer.")
                )
        new_offer = super().create(vals_list)
        new_offer.property_id.state="offer_received"
        return new_offer

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

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.bayer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
