# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class sales_report__wizard(models.Model):
    _name = 'sales_report__wizard.sales_report__wizard'
    _description = 'Sotuv hisoboti wizard'

    date_from = fields.Date(
        string='Boshlanish sanasi',
        required=True,
        default=lambda self: date.today() - timedelta(days=30)
    )

    date_to = fields.Date(
        string='Tugash sanasi',
        required=True,
        default=fields.Date.today
    )

    report_type = fields.Selection([
        ('detailed', 'Batafsil hisobot'),
        ('summary', 'Qisqa hisobot'),
        ('by_category', 'Kategoriya bo\'yicha')
    ], string='Hisobot turi', default='detailed')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from > wizard.date_to:
                raise UserError('Boshlanish sanasi tugash sanasidan keyin bo\'lishi mumkin emas!')

    def action_generate_report(self):
        orders = self.env['sale.order'].search([
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
            ('state', 'in', ['sale', 'done'])
        ])
        return {
            'name': 'Sotuv Hisoboti',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,pivot,graph',
            'domain': [('id', 'in', orders.ids)],
            'context': {
                'search_default_groupby_date': True,
                'group_by': 'date_order:month' if self.report_type == 'summary' else ''
            }
        }

    def action_print_pdf(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'report_type': self.report_type,
            'company_id': self.env.company.id
        }
        return self.env.ref('base.action_model_data').report_action(self, data=data)
