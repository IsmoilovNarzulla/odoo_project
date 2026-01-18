from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = "school.student"
    _description = "Talaba"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name asc" # Tartiblash

    student_id = fields.Char("Student ID",readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.student')
    )

    name = fields.Char("Ism", required=True, tracking=True,)
    photo = fields.Image("Photo", max_width=720, max_height=1024)
    birth_day = fields.Date("Tug'ilgan sana", tracking=True,)
    age = fields.Integer("Yoshi", compute='_compute_age', store=True)
    height = fields.Float("Bo'yi (m)", digits=(3, 2))
    phone_number = fields.Char("Telefon raqami", required=True, tracking=True,)
    email = fields.Char("Email")
    score = fields.Float("Imtihon bahosi", digits=(3, 2), tracking=True,)
    rating = fields.Integer("Reyting", tracking=True,)
    description = fields.Text("Qo'shimcha izoh",translate=True)
    bio = fields.Text("Bio")
    profile = fields.Html("Profil sahifasi")
    passport_number = fields.Char("Pasport raqami",index=True, tracking=True,)

    group_id = fields.Many2one(
        "school.group",
        "Guruh",
        ondelete="cascade",
        tracking=True,
    )

    student_ids = fields.One2many(
        "school.student",
        "group_id",
        "Talabalar"
    )

    teacher_id = fields.Many2one(
        "school.teacher",
        "Asosiy o'qituvchi",
        tracking=True,
    )

    course_ids = fields.Many2many(
        "course.kurslar",
        "student_course_rel",
        "student_id",
        "course_id",
        string="Kurslar"
    )

    state = fields.Selection([
        ('draft', 'Arizachi'),
        ('active', 'Faol talaba'),
        ('graduated', 'Bitiruvchi'),
        ('left', "O'qishni tashlagan"),
        ('alumni', 'Bitirgan'),
    ], string="Holati", default='draft', tracking=True)

    @api.depends('birth_day')
    def _compute_age(self):
        today = fields.Date.today()
        for student in self:
            if student.birth_day:
                student.age = today.year - student.birth_day.year - (
                        (today.month, today.day) < (student.birth_day.month, student.birth_day.day)
                )
            else:
                student.age = 0

    @api.constrains('phone_number')
    def _check_phone_number(self):
        for student in self:
            if student.phone_number and not student.phone_number.isdigit():
                raise ValidationError("Telefon raqami faqat raqamlardan iborat bo'lishi kerak!")

    @api.constrains('email')
    def _check_email(self):
        for student in self:
            if student.email and '@' not in student.email:
                raise ValidationError("Noto'g'ri email formati!")
