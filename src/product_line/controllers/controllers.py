# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLine(http.Controller):
#     @http.route('/product_line/product_line', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_line/product_line/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_line.listing', {
#             'root': '/product_line/product_line',
#             'objects': http.request.env['product_line.product_line'].search([]),
#         })

#     @http.route('/product_line/product_line/objects/<model("product_line.product_line"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_line.object', {
#             'object': obj
#         })

