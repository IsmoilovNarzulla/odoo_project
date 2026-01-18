# -*- coding: utf-8 -*-
# from odoo import http


# class EducationGroup(http.Controller):
#     @http.route('/education_group/education_group', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_group/education_group/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_group.listing', {
#             'root': '/education_group/education_group',
#             'objects': http.request.env['education_group.education_group'].search([]),
#         })

#     @http.route('/education_group/education_group/objects/<model("education_group.education_group"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_group.object', {
#             'object': obj
#         })

