# -*- coding: utf-8 -*-

from odoo import models, fields, api


class products(models.Model):
    _name = 'uic.product'
    _description = 'Uic product'
    _order = 'name'

    name = fields.Char('Name', required=True)
    price = fields.Float('Price',default=0.0)
    stock_qty = fields.Float('Stock Quantity',default=0.0)
    active = fields.Boolean(string='Faol', default=True)
    ono_to_one = fields.Many2one('uic.person', string='Onto to One',)
    @api.depends('price', 'stock_qty')
    def _compute_total_value(self):
        for record in self:
            record.total_value = record.price * record.stock_qty

    total_value = fields.Float(
        string='Jami qiymat',
        compute='_compute_total_value',
        store=True
    )

