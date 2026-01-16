
from odoo import models, fields

class ProductWithTracking(models.Model):
    _name = 'uic.product'
    _inherit = ['uic.product', 'uic.tracking.mixin']

