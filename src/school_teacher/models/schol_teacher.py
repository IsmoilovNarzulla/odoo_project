from email.policy import default

from odoo.odoo import models, fields, api


class Teacher(models.Model):
    _name = "school.teacher"
    _description = "O‘qituvchi"

    name = fields.Char("F.I.Sh.", required=True)
    specialty = fields.Char("Mutaxassisligi", max_length=100, required=True)
    course_price =fields.Monetary("Kurs narxi", digits=(7, 2), currency_field="currency_id", required=True)
    currency_id = fields.Many2one("res.currency", string="Summa", blank = True, null = True)
    start_date= fields.Date("Boshlanish sanasi", required=True)
    lesson_start = fields.Datetime("Dars boshlanishi", required=True)
    bio = fields.Text("Tarjimai hol", maxlength=1000)
    phone_number = fields.Char("Tel raqami xalqaro formatda kriting", required=True)
    email = fields.Char("Email", blank=True,null=True)
    profile = fields.Html("Profil sahifasi")
    status = fields.Char(default = "Active")