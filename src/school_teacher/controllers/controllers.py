# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolTeacher(http.Controller):
#     @http.route('/school_teacher/school_teacher', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_teacher/school_teacher/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_teacher.listing', {
#             'root': '/school_teacher/school_teacher',
#             'objects': http.request.env['school_teacher.school_teacher'].search([]),
#         })

#     @http.route('/school_teacher/school_teacher/objects/<model("school_teacher.school_teacher"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_teacher.object', {
#             'object': obj
#         })

