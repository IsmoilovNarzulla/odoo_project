from odoo import models, fields


class OperationLog(models.Model):
    _name = 'operation.log'
    _description = 'Operatsiyalar Logi'
    _order = 'create_date desc'


    name = fields.Char(string="Operatsiya Nomi", required=True)
    model_name = fields.Char(string="Model Nomi", required=True)
    record_id = fields.Integer(string="Yozuv IDsi")
    record_name = fields.Char(string="Yozuv Nomi")
    operation_type = fields.Selection([
        ('create', 'Yaratish'),
        ('write', 'Yangilash'),
        ('unlink', 'O\'chirish'),
        ('read', 'O\'qish')
    ], string="Operatsiya Turi")
    user_id = fields.Many2one(
        'res.users',
        string="Foydalanuvchi",
        default=lambda self: self.env.user
    )
    old_values = fields.Text(string="Eski Qiymatlar")
    new_values = fields.Text(string="Yangi Qiymatlar")
    ip_address = fields.Char(string="IP Manzil")
    create_date = fields.Datetime(string="Vaqt", default=fields.Datetime.now)