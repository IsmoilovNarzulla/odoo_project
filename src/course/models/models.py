# -*- coding: utf-8 -*-

from odoo import models, fields


class course(models.Model):
    _name = 'course.course'
    _description = 'Kurs'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Kurs nomi", required=True, tracking=True)
    group =fields.Char("Guruh nomi", required=True, tracking=True)
    course_price =fields.Monetary("Kurs narxi", digits=(7, 2), currency_field="currency_id", required=True)
    currency_id = fields.Many2one("res.currency", string="Valyuta", blank = True, null = True)
    start_date= fields.Date("Boshlanish sanasi", required=True, tracking=True)
    lesson_start = fields.Datetime("Dars boshlanishi", required=True, tracking=True)

    teacher_id = fields.Many2one(
        "school.teacher",
        "O'qituvchi",
        required=True
    )

    student_ids = fields.Many2many(
        "school.student",
        "student_course_rel",
        "course_id",
        "student_id",
        string="Talabalar"
    )

    group_id = fields.Many2one(
        "school.group",
        "Guruh"
    )