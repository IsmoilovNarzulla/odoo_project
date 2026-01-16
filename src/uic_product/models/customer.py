
from odoo import models, fields

class Customer(models.Model):
    _name = 'uic.customer'
    _description = 'Mijoz'
    _inherit = ['uic.timestamp.mixin', 'uic.contact.mixin']

    name = fields.Char(string='Mijoz nomi', required=True)
    code = fields.Char(string='Mijoz kodi', required=True)
    discount = fields.Float(string='Chegirma %', default=0.0)
    credit_limit = fields.Float(string='Kredit limiti')


    def calculate_discount(self, amount):
        return amount * (self.discount / 100)