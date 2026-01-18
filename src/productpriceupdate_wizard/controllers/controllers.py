# -*- coding: utf-8 -*-
# from odoo import http


# class ProductpriceupdateWizard(http.Controller):
#     @http.route('/productpriceupdate_wizard/productpriceupdate_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/productpriceupdate_wizard/productpriceupdate_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('productpriceupdate_wizard.listing', {
#             'root': '/productpriceupdate_wizard/productpriceupdate_wizard',
#             'objects': http.request.env['productpriceupdate_wizard.productpriceupdate_wizard'].search([]),
#         })

#     @http.route('/productpriceupdate_wizard/productpriceupdate_wizard/objects/<model("productpriceupdate_wizard.productpriceupdate_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('productpriceupdate_wizard.object', {
#             'object': obj
#         })

