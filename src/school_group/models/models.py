# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolGroup(models.Model):
    _name = "school.group"
    _description = "Guruh"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Guruh nomi", required=True)
    code = fields.Char("Guruh kodi", required=True)

    course_id = fields.Many2one(
        "course.kurslar",
        "Kurs",
        required=True,
        ondelete="cascade",
        tracking=True
    )
    # teacher_id = fields.Many2one(
    #     "school.teacher",
    #     "Guruh rahbari",
    #     tracking=True
    # )

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

    state = fields.Selection([
        ('draft', 'Dasturiy'),
        ('active', 'Faol'),
        ('completed', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan'),
    ], string="Holati", default='draft', tracking=True)

    @api.depends('student_ids')
    def _compute_current_count(self):
        for group in self:
            group.current_count = len(group.student_ids)

    @api.constrains('student_ids')
    def _check_capacity(self):
        for group in self:
            if len(group.student_ids) > group.capacity:
                raise ValidationError(
                    f"Guruh sig'imi {group.capacity} talaba. "
                    f"Hozir {len(group.student_ids)} talaba bor!"
                )

