# -*- coding: utf-8 -*-

from odoo.odoo import models, fields, api


class document(models.Model):
    _name = 'school.document'
    _description = 'Talaba hujjatlari'

    name = fields.Char("Hujjat nomi", required= True ,index=True)
    file_type = fields.Binary("Fayl")
    file_name = fields.Char("Fayl nomi", required= True ,index=True)


    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

