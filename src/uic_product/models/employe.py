
from odoo import models, fields, api


class Employee(models.Model):
    _name = 'uic.employee'
    _description = 'Xodim'
    _inherit = {'uic.person': 'person_id'}

    person_id = fields.Many2one(
        'uic.person',
        string='Shaxs ma\'lumotlari',
        required=True,
        ondelete='cascade'
    )


    employee_id = fields.Char(string='Xodim ID', required=True)
    department = fields.Selection([
        ('sales', 'Sotuv'),
        ('purchase', 'Xarid'),
        ('accounting', 'Buxgalteriya'),
        ('warehouse', 'Ombor'),
        ('management', 'Rahbariyat')
    ], string='Bo\'lim')
    salary = fields.Float(string='Oylik maosh')
    hire_date = fields.Date(string='Ishga kirgan sana')

    @api.model
    def create(self, vals):
        person_vals = {
            'name': vals.get('name'),
            'phone': vals.get('phone'),
            'email': vals.get('email'),
            'address': vals.get('address'),
            'birth_date': vals.get('birth_date'),
            'gender': vals.get('gender'),
        }

        for key in person_vals.copy():
            if key in vals:
                del vals[key]

        person = self.env['uic.person'].create(person_vals)
        vals['person_id'] = person.id

        return super(Employee, self).create(vals)