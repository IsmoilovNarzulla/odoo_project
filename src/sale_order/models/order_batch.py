from odoo import models, fields


class OrderBatchOperation(models.Model):
    _inherit = 'sale.order'

    def update_prices_batch(self):
        old_orders = self.search([
            ('date_order', '<', '2024-01-01'),
            ('state', 'in', ['draft', 'sent'])
        ])
        old_orders.write({
            'validity_date': fields.Date.today(),
            'note': 'Eski buyurtma - narxlar yangilandi',
        })

        for order in old_orders:
            order.order_line.write({
                'discount': 5,
            })

    def update_order_status(self, new_status):
        self.write({
            'state': new_status,
            'last_update': fields.Datetime.now(),
            'updated_by': self.env.user.id,
        })

        self.env['order.audit.log'].create({
            'order_id': self.id,
            'old_state': self._origin.state,
            'new_state': new_status,
            'user_id': self.env.user.id,
            'change_date': fields.Datetime.now(),
        })