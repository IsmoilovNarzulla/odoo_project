
from odoo import models, fields, api

class TimeStampMixin(models.AbstractModel):
    _name = 'uic.timestamp.mixin'
    _description = 'Timestamp Mixin'

    created_at = fields.Datetime(
        string='Yaratilgan',
        default=fields.Datetime.now,
        readonly=True
    )
    updated_at = fields.Datetime(
        string='Yangilangan',
        default=fields.Datetime.now,
        readonly=True
    )

    @api.model
    def create(self, vals):
        vals['created_at'] = fields.Datetime.now()
        vals['updated_at'] = fields.Datetime.now()
        return super(TimeStampMixin, self).create(vals)

    def write(self, vals):
        vals['updated_at'] = fields.Datetime.now()
        return super(TimeStampMixin, self).write(vals)


class ContactInfoMixin(models.AbstractModel):
    _name = 'uic.contact.mixin'
    _description = 'Contact Information Mixin'

    phone = fields.Char(string='Telefon')
    email = fields.Char(string='Email')
    address = fields.Text(string='Manzil')

    def send_email(self, subject, body):
        for record in self:
            if record.email:
                print(f"{subject} - {body} -> {record.email}")
        return True