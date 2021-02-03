# Copyright 2021 Ecosoft
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import Form, SavepointCase


class TestRequestsCommon(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Define a request category for purchase.
        request_category_form = Form(cls.env["request.category"])
        request_category_form.name = "Product Request"
        request_category_form.request_type = "purchase"
        cls.purchase_category = request_category_form.save()
        # Create an user we can use as approver for example.
        cls.user_approver = cls.env["res.users"].create(
            {
                "login": "yesman",
                "name": "Carl Allen",
            }
        )
        # Create partners to use as seller.
        cls.partner_seller_1 = cls.env["res.partner"].create(
            {"name": "Uncle Bill's Electronic Store"}
        )
        cls.partner_seller_2 = cls.env["res.partner"].create(
            {"name": "Jawa Good Deals"}
        )
        # Create some products.
        cls.product_mouse = cls.env["product.product"].create(
            {
                "name": "Computer Mouse",
            }
        )
        cls.product_computer = cls.env["product.product"].create(
            {
                "name": "Laptop",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.partner_seller_1.id,
                            "min_qty": 1,
                            "price": 250,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.partner_seller_2.id,
                            "min_qty": 1,
                            "price": 260,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.partner_seller_2.id,
                            "min_qty": 10,
                            "price": 230,
                        },
                    ),
                ],
            }
        )
        cls.product_earphone = cls.env["product.product"].create(
            {
                "name": "Earphone",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.partner_seller_1.id,
                            "min_qty": 1,
                            "price": 8,
                        },
                    ),
                ],
            }
        )
        # Find UoM unit and create the 'fortnight' unit.
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_fortnight = cls.env["uom.uom"].create(
            {
                "category_id": cls.uom_unit.category_id.id,
                "name": "Fortnights",
                "uom_type": "bigger",
                "factor_inv": 15.0,
            }
        )

    def create_request_form(self, approver=False, category=False):
        """Return a new instance of Form for a purchase request.

        :param approver: optional record to set an approver directly on the new
            request request.
        :param category: optional record to chose the category of the new
            request request. Take the "Product Request" by default.
        """
        if not category:
            category = self.purchase_category
        create_request_form = Form(
            self.env["request.request"].with_context(
                default_name=self.purchase_category.name,
                default_category_id=category.id,
            )
        )
        if approver:
            # Set an approver.
            with create_request_form.approver_ids.new() as req_approver:
                req_approver.user_id = approver
        return create_request_form

    def create_purchase_order(self, partner=False, origin=False, lines=False):
        """Create and return a new purchase order.

        :param recort partner: partner used as vendor ('partner_seller_1' by default).
        :param string origin: optional string to define a purchase order's origin.
        :param list lines: optional list containing dicts to create purchase lines.
               Take the following keys:
                - product: record of the product
                - price: unit price for the product
                - quantity: 1 by default
                - uom: uom id for the line (product's uom by default)
        """
        vals = {
            "partner_id": (partner and partner.id) or self.partner_seller_1.id,
            "origin": origin,
        }
        # Create order lines if defined.
        if lines:
            vals["order_line"] = []
            for line in lines:
                product = line["product"]
                order_line_vals = (
                    0,
                    0,
                    {
                        "date_planned": fields.Date.today(),
                        "name": product.display_name,
                        "price_unit": line["price"],
                        "product_id": product.id,
                        "product_qty": line.get("quantity", 1),
                        "product_uom": line.get("uom", product.uom_id.id),
                    },
                )
                vals["order_line"].append(order_line_vals)

        new_purchase = self.env["purchase.order"].create(vals)
        return new_purchase

    def get_purchase_order(self, request, index=0):
        purchases = request.product_line_ids.purchase_order_line_id.order_id
        return purchases[index]
