# -*- coding: utf-8 -*-

from odoo import models, fields, api


class productpriceupdate_wizard(models.Model):
    _name = 'productpriceupdate_wizard.productpriceupdate_wizard'
    _description = 'Mahsulot narxlarini yangilash uchun wizard'

    percentage = fields.Float(
        string='Foiz (%)',
        required=True,
        default=10.0,
        help='Narxlarni oshirish foizi'
    )

    category_id = fields.Many2one(
        'productpriceupdate_wizard.productpriceupdate_wizard',
        string='Mahsulot Kategoriyasi',
        help='Agar tanlansa, faqat shu kategoriyadagi mahsulotlar yangilanadi'
    )

    def action_update_prices(self):
        active_ids = self.env.context.get('active_ids', [])
        products = self.env['productpriceupdate_wizard.productpriceupdate_wizard'].browse(active_ids)
        if self.category_id:
            products = products.filtered(lambda p: p.categ_id == self.category_id)
        for product in products:
            new_price = product.list_price * (1 + self.percentage / 100)
            product.write({'list_price': new_price})

        return {
            'type': 'ir.actions.act_window_close',
            'context': {'updated_count': len(products)}
        }
