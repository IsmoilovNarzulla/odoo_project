from odoo.odoo import models, fields, api


class Student(models.Model):
    _name = "school.student"
    _description = "Talaba"

    student_id = fields.Char("Student ID", readonly=True)
    name = fields.Char("Ism", maxlength=50)
    brith_day = fields.Date("Tug'ilgan sana")
    age = fields.Integer("Yoshi")
    height = fields.Float("Bo'yi (m)", digits=(3, 2))
    phone_number = fields.Char("Telefon raqami ", required=True)
    email = fields.Char("Email",blank=True,null=True)
    score = fields.Float("Imtihon bahosi", digits=(3, 2))
    rating = fields.Integer("Reyting")
    description = fields.Text("Qo'shimcha izoh", maxlength=200, translate=True)
    bio = fields.Text("Bio", maxlength=10000)
    profile = fields.Html("Profil sahifasi")
    passport_number = fields.Char(index=True)