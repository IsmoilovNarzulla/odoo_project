# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolGroup(http.Controller):
#     @http.route('/school_group/school_group', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_group/school_group/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_group.listing', {
#             'root': '/school_group/school_group',
#             'objects': http.request.env['school_group.school_group'].search([]),
#         })

#     @http.route('/school_group/school_group/objects/<model("school_group.school_group"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_group.object', {
#             'object': obj
#         })

