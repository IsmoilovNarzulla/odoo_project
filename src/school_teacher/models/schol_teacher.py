from email.policy import default

from odoo import models, fields, api


class Teacher(models.Model):
    _name = "school.teacher"
    _description = "O‘qituvchi"

    name = fields.Char("F.I.Sh.", required=True)
    specialty = fields.Char("Mutaxassisligi", max_length=100, required=True)
    bio = fields.Text("Tarjimai hol", maxlength=1000)
    phone_number = fields.Char("Tel raqami xalqaro formatda kriting", required=True)
    email = fields.Char("Email", blank=True,null=True)
    profile = fields.Html("Profil sahifasi")
    status = fields.Selection([
        ('active', 'Faol'),
        ('inactive', 'Faol emas'),
        ('vacation', 'Taʼtil'),
    ], string="Holati", default='active')

    course_ids = fields.One2many(
        "course.course",
        "teacher_id",
        string="O'qitayotgan kurslar"
    )

    student_ids = fields.Many2many(
        "school.student",
        "teacher_student_rel",
        "teacher_id",
        "student_id",
        string="Talabalar"
    )