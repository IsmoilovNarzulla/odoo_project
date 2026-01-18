# -*- coding: utf-8 -*-
# from odoo import http


# class ContactexportWizard(http.Controller):
#     @http.route('/contactexport_wizard/contactexport_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contactexport_wizard/contactexport_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contactexport_wizard.listing', {
#             'root': '/contactexport_wizard/contactexport_wizard',
#             'objects': http.request.env['contactexport_wizard.contactexport_wizard'].search([]),
#         })

#     @http.route('/contactexport_wizard/contactexport_wizard/objects/<model("contactexport_wizard.contactexport_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contactexport_wizard.object', {
#             'object': obj
#         })

