
from odoo import models, fields, api

class TrackingMixin(models.Model):
    _name = 'uic.tracking.mixin'
    _description = 'Tracking Mixin'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    created_by = fields.Many2one(
        'res.users',
        string='Yaratuvchi',
        default=lambda self: self.env.user,
        readonly=True
    )
    created_date = fields.Datetime(
        string='Yaratilgan sana',
        default=fields.Datetime.now,
        readonly=True
    )

