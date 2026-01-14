# -*- coding: utf-8 -*-
# from odoo import http


# class MyModel(http.Controller):
#     @http.route('/my_model/my_model', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_model/my_model/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_model.listing', {
#             'root': '/my_model/my_model',
#             'objects': http.request.env['my_model.my_model'].search([]),
#         })

#     @http.route('/my_model/my_model/objects/<model("my_model.my_model"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_model.object', {
#             'object': obj
#         })

