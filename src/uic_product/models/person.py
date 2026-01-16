
from odoo import models, fields

class Person(models.Model):
    _name = 'uic.person'
    _description = 'Person'
    _order = 'name'

    name = fields.Char(string='Ism', required=True)
    birth_date = fields.Date(string='Tug\'ilgan sana')
    gender = fields.Selection([
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    ], string='Jinsi')


    phone = fields.Char(string='Telefon')
    email = fields.Char(string='Email')
    address = fields.Text(string='Manzil')


    passport = fields.Char(string='Pasport raqami')
    tin = fields.Char(string='STIR')