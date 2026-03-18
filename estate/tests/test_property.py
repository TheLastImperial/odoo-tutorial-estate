import logging

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form

from odoo import Command

_logger = logging.getLogger(__name__)

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.partner = cls.env['res.partner'].create({
            'name': 'Seller'
        })
        cls.properties = cls.env['estate.property'].create([{
            'name': 'Test Property',
            'state': 'new',
            'description': 'Description',
            'postcode': 8000,
            'date_availability': '2020-01-01',
            'expected_price': 20000,
            'bedrooms': 2,
            'living_area': 10,
            'facades': 4,
            'garage': True,
            'garden': True,
            'garden_area': 10,
            'garden_orientation': 'south',
            'offer_ids': [
                Command.create({
                    'partner_id': cls.partner.id,
                    'price': 20000,
                    'validity': 14
                }),
            ]
        }])
        _logger.info("Database created")

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.assertRecordValues(self.properties, [
           {'total_area': 20},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
           {'state': 'sold'},
        ])

        # with self.assertRaises(UserError):
        #     self.properties.forbidden_action_on_sold_property()
    def test_checkbox_garden(self):
        form = Form(self.env['estate.property'])
        form.garden = True
        form.garden_area = 10
        form.garden_orientation = "north"
        self.assertEqual(form.total_area, 10)
        _logger.info("Total area validated")

        self.assertEqual(form.garden_orientation, "north")
        _logger.info("Garden orientation validated")

        form.garden = False
        self.assertEqual(form.total_area, 0)
        _logger.info("Uncheck garden validated")

        self.assertEqual(form.garden_orientation, False)
        _logger.info("Uncheck garden. Orientation validated")
