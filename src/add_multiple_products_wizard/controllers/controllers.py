# -*- coding: utf-8 -*-
# from odoo import http


# class AddMultipleProductsWizard(http.Controller):
#     @http.route('/add_multiple_products_wizard/add_multiple_products_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_multiple_products_wizard/add_multiple_products_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_multiple_products_wizard.listing', {
#             'root': '/add_multiple_products_wizard/add_multiple_products_wizard',
#             'objects': http.request.env['add_multiple_products_wizard.add_multiple_products_wizard'].search([]),
#         })

#     @http.route('/add_multiple_products_wizard/add_multiple_products_wizard/objects/<model("add_multiple_products_wizard.add_multiple_products_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_multiple_products_wizard.object', {
#             'object': obj
#         })

