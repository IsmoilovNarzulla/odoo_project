# -*- coding: utf-8 -*-
# from odoo import http


# class SalesReportWizard(http.Controller):
#     @http.route('/sales_report__wizard/sales_report__wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_report__wizard/sales_report__wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_report__wizard.listing', {
#             'root': '/sales_report__wizard/sales_report__wizard',
#             'objects': http.request.env['sales_report__wizard.sales_report__wizard'].search([]),
#         })

#     @http.route('/sales_report__wizard/sales_report__wizard/objects/<model("sales_report__wizard.sales_report__wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_report__wizard.object', {
#             'object': obj
#         })

