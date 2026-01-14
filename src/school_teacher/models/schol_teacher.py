from email.policy import default

from odoo import models, fields, api


class Teacher(models.Model):
    _name = "school.teacher"
    _description = "O‘qituvchi"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc"

    teacher_id = fields.Char("Teacher ID",readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.teacher')
    )

    name = fields.Char("F.I.Sh.", required=True,tracking=True,)
    specialty = fields.Char("Mutaxassisligi", max_length=100, required=True,tracking=True,)
    bio = fields.Text("Tarjimai hol", maxlength=1000)
    phone_number = fields.Char("Tel raqami xalqaro formatda kriting", required=True,tracking=True,)
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

    group_ids = fields.One2many(
        "school.group",
        "teacher_id",
        string="Rahbarlik qilayotgan guruhlar"
    )

    total_students = fields.Integer(
        "Jami talabalar",
        compute='_compute_total_students',
        store=True
    )

    @api.depends('student_ids')
    def _compute_total_students(self):
        for teacher in self:
            teacher.total_students = len(teacher.student_ids)