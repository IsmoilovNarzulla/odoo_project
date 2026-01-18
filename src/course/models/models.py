# -*- coding: utf-8 -*-

from odoo import models, fields, api


class course(models.Model):
    _name = 'course.kurslar'
    _description = 'Kurs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Kurs nomi", required=True, tracking=True)
    group =fields.Char("Guruh nomi", required=True, tracking=True)
    course_price =fields.Float("Kurs narxi", digits=(10,2), currency_field="currency_id", required=True)
    currency_id = fields.Many2one("res.currency", string="Valyuta",)
    start_date= fields.Date("Boshlanish sanasi", required=True, tracking=True)
    lesson_start = fields.Datetime("Dars boshlanishi", required=True, tracking=True)

    # teacher_id = fields.Many2one(
    #     "school.teacher",
    #     "O'qituvchi",
    #     required=True,
    #     tracking=True
    # )

    student_ids = fields.Many2many(
        "school.student",
        "student_course_rel",
        "course_id",
        "student_id",
        string="Talabalar"
    )

    group_id = fields.Many2one(
        "school.group",
        "Guruh",
        tracking=True
    )

    student_count = fields.Integer(
        "Talabalar soni",
        compute='_compute_student_count',
        store=True
    )

    @api.depends('student_ids')
    def _compute_student_count(self):
        for course in self:
            course.student_count = len(course.student_ids)