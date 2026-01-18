from odoo import models, api
from odoo.exceptions import ValidationError


class AdvancedOrderManagement(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.custom')
        result = super().create(vals)
        result._post_create_actions()
        return result


    def write(self, vals):
        old_values = {rec.id: rec.read()[0] for rec in self}
        result = super().write(vals)
        self._log_changes(old_values, vals)
        return result

    def unlink(self):
        for order in self:
            if order.state == 'done':
                raise ValidationError("Bajarilgan buyurtmani o‘chirib bo‘lmaydi!")
            if order.invoice_ids:
                raise ValidationError("Hisob-fakturasi bor buyurtmani o‘chirib bo‘lmaydi!")
        return super().unlink()


    def duplicate_order(self):
        for order in self:
            new_order_vals = order.copy_data()[0]
            new_order_vals['name'] = f"{order.name}-COPY"
            new_order = self.create(new_order_vals)
            for line in order.order_line:
                line.copy({'order_id': new_order.id})

        return new_order