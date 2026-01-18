# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from odoo import models, fields, api

_logger = logging.getLogger(__name__)
class res_partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def cleanup_inactive_partners(self):
        partners = self.search([("active", "=", False)])
        count = len(partners)

        if partners:
            partners.unlink()

        _logger.info("%s ta inactive partner o‘chirildi. Vaqt: %s", count, datetime.now())
