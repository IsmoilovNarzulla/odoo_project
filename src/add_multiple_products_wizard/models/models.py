# -*- coding: utf-8 -*-

from odoo import models, fields, api


class add_multiple_products_wizard(models.TransientModel):
    _name = 'add_multiple_products_wizard.add_multiple_products_wizard'
    # _description = 'Bir nechta mahsulot qoshish wizard',
    order_id = fields.Many2one('sale.order', string='Buyurtma')

    product_id = fields.Many2one('product.product', string='Mahsulot')
    quantity = fields.Float(string='Miqdor', default=1.0)
    price_unit = fields.Float(string='Narx')

    product_lines = fields.One2many(
        'add.multiple.products.wizard.line',
        'wizard_id',
        string='Mahsulotlar'
    )

    def action_add_products(self):
        for wizard in self:
            for line in self.product_lines:
                self.env['sale.order.line'].create({
                    'order_id': self.order_id.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                })
        return {'type': 'ir.actions.act_window_close'}

class AddMultipleProductsWizardLine(models.TransientModel):
    _name = 'add.multiple.products.wizard.line'
    _description = 'Wizard liniyasi'
    wizard_id = fields.Many2one('add_multiple_products_wizard.add_multiple_products_wizard')
    product_id = fields.Many2one('product.product', string='Mahsulot', required=True)
    quantity = fields.Float(string='Miqdor', default=1.0)
    price_unit = fields.Float(string='Narx')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price

