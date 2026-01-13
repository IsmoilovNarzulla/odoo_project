from odoo import models, fields, api


class Student(models.Model):
    _name = "school.student"
    _description = "Talaba"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Char("Student ID", readonly=True)
    name = fields.Char("Ism", max_length=50, required=True)
    photo = fields.Image("Photo", max_width=720, max_height=1024)
    birth_day = fields.Date("Tug'ilgan sana")
    age = fields.Integer("Yoshi", compute='_compute_age', store=True)
    height = fields.Float("Bo'yi (m)", digits=(3, 2))
    phone_number = fields.Char("Telefon raqami", required=True)
    email = fields.Char("Email")
    score = fields.Float("Imtihon bahosi", digits=(3, 2))
    rating = fields.Integer("Reyting")
    description = fields.Text("Qo'shimcha izoh", max_length=200, translate=True)
    bio = fields.Text("Bio", max_length=10000)
    profile = fields.Html("Profil sahifasi")
    passport_number = fields.Char(index=True)

    group_id = fields.Many2one(
        "school.group",
        "Guruh",
        ondelete="cascade",
    )

    student_ids = fields.One2many(
        "school_student.Student",
        "group_id",
        "Talabalar"
    )

    teacher_id = fields.Many2one(
        "school.teacher",
        "Asosiy o'qituvchi"
    )

    course_ids = fields.Many2many(
        "course.course",
        "student_course_rel",
        "student_id",
        "course_id",
        string="Kurslar"
    )

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
