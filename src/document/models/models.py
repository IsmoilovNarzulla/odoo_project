# -*- coding: utf-8 -*-

from odoo import models, fields, api


class document(models.Model):
    _name = 'school.document'
    _description = 'Talaba hujjatlari'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Hujjat nomi", required= True ,index=True,tracking=True)
    file_type = fields.Binary("Fayl",attachment=True)
    file_name = fields.Char("Fayl nomi",index=True,tracking=True)


    student_id = fields.Many2one(
        "school.student",
        "Talaba",
        required=True,
        ondelete="cascade",
        tracking=True
    )

    document_type = fields.Selection([
        ('passport', 'Pasport'),
        ('diploma', 'Diploma'),
        ('certificate', 'Sertifikat'),
        ('photo', 'Rasm'),
        ('other', 'Boshqa'),
    ], string="Hujjat turi", required=True, default='other', tracking=True)

    upload_date = fields.Datetime(
        "Yuklangan sana",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )

    uploaded_by = fields.Many2one(
        "res.users",
        "Yuklovchi",
        default=lambda self: self.env.user,
        readonly=True
    )

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

