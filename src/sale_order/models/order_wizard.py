from odoo import models, fields


class OrderWizard(models.TransientModel):
    _name = 'demo.order.wizard'

    def create_multiple_orders(self):
        customer_ids = self.env['res.partner'].search([('customer', '=', True)], limit=5)

        orders_to_create = []
        for i, customer in enumerate(customer_ids, 1):
            order_vals = {
                'partner_id': customer.id,
                'date_order': fields.Date.today(),
                'name': f'AUTO-ORDER-{i:03d}',
                'order_line': [
                    (0, 0, {
                        'product_id': self.product_id.id,
                        'product_uom_qty': 1,
                        'price_unit': 1000,
                    })
                ]
            }
            orders_to_create.append(order_vals)


        created_orders = self.env['sale.order'].create(orders_to_create)


        return {
            'type': 'ir.actions.act_window',
            'name': 'Yaratilgan buyurtmalar',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', created_orders.ids)],
        }