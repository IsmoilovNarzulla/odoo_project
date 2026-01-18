
from odoo import models, fields, api

class TrackingMixin(models.AbstractModel):
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


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['created_by'] = self.env.user.id
            vals['created_date'] = fields.Datetime.now()
        return super(TrackingMixin, self).create(vals_list)