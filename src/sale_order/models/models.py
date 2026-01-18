# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class sale_order(models.Model):
    _inherit = "sale.order"

    def apply_discount(self, percent=0):
        for order in self:
            for line in order.order_line:
                line.discount = percent


    def calculate_total_with_tax(self):
        total = self.amount_total
        tax_amount = total * 0.15  # 15% soliq
        return total + tax_amount

    def validate_and_approve(self):
        if self.amount_total <= 0:
            raise ValidationError("Buyurtma summasi noldan katta bo'lishi kerak!")

        if not self.order_line:
            raise ValidationError("Buyurtmada mahsulotlar bo'lishi kerak!")

        self.state = 'approved'
        return True



