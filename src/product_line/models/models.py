# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product_line(models.Model):
    _name = 'product_line.product_line'
    _description = 'Product Line for Training'

    product_name = fields.Char(string="Product Name", required=True)
    price = fields.Float(string="Price")
    quantity = fields.Integer(string="Quantity", default=1)

    total_price = fields.Float(
        string="Total Price",
        compute="_compute_total_price"
    )

    field_name = fields.Float(
        string="Some Field",
        compute="_compute_method",
        store=False,
    )

    @api.depends('price', 'quantity')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.price * record.quantity

