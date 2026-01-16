
from odoo import models, fields, api


class ProductExtension(models.Model):
    _inherit = 'uic.product'

    barcode = fields.Char(string='Shtrix kod')
    weight = fields.Float(string='Vazni (kg)')
    category = fields.Selection([
        ('electronics', 'Elektronika'),
        ('clothing', 'Kiyim-kechak'),
        ('other', 'Boshqa')
    ], string='Kategoriya', default='other')

    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            vals['barcode'] = self.env['ir.sequence'].next_by_code('product.barcode')
        return super(ProductExtension, self).create(vals)