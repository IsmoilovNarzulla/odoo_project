
from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'uic.sale.order'
    _description = 'Sotuv buyurtmasi'
    _inherit = ['mail.thread', 'uic.timestamp.mixin']
    _order = 'date_order desc'
    _inherits = {'res.partner': 'partner_id'}
    name = fields.Char(
        string='Buyurtma raqami',
        default=lambda self: self.env['ir.sequence'].next_by_code('sale.order'),
        readonly=True
    )

    date_order = fields.Datetime(
        string='Buyurtma sanasi',
        default=fields.Datetime.now,
        required=True
    )


    partner_id = fields.Many2one(
        'res.partner',
        string='Mijoz',
        required=True,
        ondelete='cascade'
    )


    order_line_ids = fields.One2many(
        'uic.sale.order.line',
        'order_id',
        string='Buyurtma qatorlari'
    )


    @api.depends('order_line_ids.price_total')
    def _compute_amount(self):
        for order in self:
            order.amount_total = sum(line.price_total for line in order.order_line_ids)
            order.amount_tax = sum(line.price_tax for line in order.order_line_ids)

    amount_total = fields.Float(
        string='Jami',
        compute='_compute_amount',
        store=True
    )
    amount_tax = fields.Float(
        string='Jami soliq',
        compute='_compute_amount',
        store=True
    )


    state = fields.Selection([
        ('draft', 'Qoralama'),
        ('confirmed', 'Tasdiqlangan'),
        ('done', 'Bajarilgan'),
        ('canceled', 'Bekor qilingan')
    ], string='Holat', default='draft')


    def action_confirm(self):
        for order in self:
            if order.state != 'draft':
                raise UserError('Faqat qoralama holatdagilarni tasdiqlash mumkin!')
            for line in order.order_line_ids:
                if line.product_id.stock_qty < line.product_uom_qty:
                    raise UserError(
                        f"Mahsulot {line.product_id.name} yetarli emas! "
                        f"Mavjud: {line.product_id.stock_qty}, Talab: {line.product_uom_qty}"
                    )

            order.state = 'confirmed'
            order.message_post(
                body="Buyurtma tasdiqlandi",
                subject="Buyurtma tasdiqlandi"
            )

        return True


class SaleOrderLine(models.Model):
    _name = 'uic.sale.order.line'
    _description = 'Sotuv buyurtmasi qatori'
    _inherit = 'uic.timestamp.mixin'

    order_id = fields.Many2one(
        'uic.sale.order',
        string='Buyurtma',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'uic.product',
        string='Mahsulot',
        required=True
    )

    product_uom_qty = fields.Float(
        string='Miqdor',
        required=True,
        default=1.0
    )

    price_unit = fields.Float(
        string='Narx',
        required=True
    )

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_total = line.product_uom_qty * line.price_unit
            line.price_tax = line.price_total * 0.15

    price_total = fields.Float(
        string='Jami',
        compute='_compute_amount',
        store=True
    )

    price_tax = fields.Float(
        string='Soliq',
        compute='_compute_amount',
        store=True
    )