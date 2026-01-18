
from odoo import models, fields

class Partner(models.Model):
    _name = 'uic.partner'
    _description = 'Hamkor'
    _inherit = {'uic.person': 'person_id'}

    person_id = fields.Many2one(
        'uic.person',
        string='Shaxs ma\'lumotlari',
        required=True,
        ondelete='cascade'
    )


    partner_type = fields.Selection([
        ('supplier', 'Ta\'minotchi'),
        ('customer', 'Mijoz'),
        ('both', 'Ikkalasi ham')
    ], string='Hamkor turi', required=True)

    company_name = fields.Char(string='Kompaniya nomi')
    vat = fields.Char(string='VAT raqami')
    credit_limit = fields.Float(string='Kredit limiti')
    payment_term = fields.Selection([
        ('net15', 'NET 15 kun'),
        ('net30', 'NET 30 kun'),
        ('net60', 'NET 60 kun'),
        ('immediate', 'Darhol')
    ], string='To\'lov muddati', default='net30')