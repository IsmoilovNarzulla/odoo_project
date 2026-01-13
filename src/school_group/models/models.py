# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolGroup(models.Model):
    _name = "school.group"
    _description = "Guruh"

    name = fields.Char("Guruh nomi", required=True)
    code = fields.Char("Guruh kodi", required=True)
    course_id = fields.Many2one(
        "course.course",
        "Kurs",
        required=True
    )
    teacher_id = fields.Many2one(
        "school.teacher",
        "Guruh rahbari"
    )
    student_ids = fields.One2many(
        "school.student",
        "group_id",
        "Talabalar"
    )
    capacity = fields.Integer("Talabalar soni chegarasi", default=30)
    current_count = fields.Integer(
        "Joriy talabalar soni",
        compute='_compute_current_count',
        store=True
    )

    @api.depends('student_ids')
    def _compute_current_count(self):
        for group in self:
            group.current_count = len(group.student_ids)

