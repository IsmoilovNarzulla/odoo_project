# -*- coding: utf-8 -*-
# from odoo import http


# class CustomProducts(http.Controller):
#     @http.route('/custom_products/custom_products', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_products/custom_products/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_products.listing', {
#             'root': '/custom_products/custom_products',
#             'objects': http.request.env['custom_products.custom_products'].search([]),
#         })

#     @http.route('/custom_products/custom_products/objects/<model("custom_products.custom_products"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_products.object', {
#             'object': obj
#         })

