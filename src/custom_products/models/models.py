from odoo import models, fields, api
from odoo.exceptions import ValidationError


class custom_products(models.Model):
    _name = "custom_products"
    _description = "Custom Product"
    # _inherit = ["audit.mixin"]
    name = fields.Char(string="Mahsulot Nomi", required=True)
    amount = fields.Float(string="Miqdor")
    state = fields.Selection([
        ('draft', 'Qoralama'),
        ('confirmed', 'Tasdiqlangan'),
        ('done', 'Yakunlangan')
    ], default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('amount', 0) < 0:
                raise ValidationError("Miqdor manfiy bo'lishi mumkin emas!")
        return super(custom_products, self).create(vals_list)


    def write(self, vals):
        if 'amount' in vals and vals['amount'] < 0:
            raise ValidationError("Miqdor manfiy bo'lishi mumkin emas!")
        if self.filtered(lambda r: r.state == 'done'):
            raise ValidationError("Yakunlangan mahsulotni o'zgartirish mumkin emas!")
        return super(custom_products, self).write(vals)


    def unlink(self):
        if self.filtered(lambda r: r.state == 'done'):
            raise ValidationError("Yakunlangan mahsulotni o'chirish mumkin emas!")
        return super(custom_products, self).unlink()
