# -*- coding: utf-8 -*-

from odoo import models, fields, api


class education_group(models.Model):
    _name = 'education_group.education_group'
    _description = 'Oʻquv guruhi'

    name = fields.Char('Guruh nomi', required=True)
    code = fields.Char('Guruh kodi')
    start_date = fields.Date('Boshlanish sanasi')
    end_date = fields.Date('Tugash sanasi')
    teacher_id = fields.Many2one('res.partner', 'Oʻqituvchi')
    student_ids = fields.One2many('education.student', 'group_id', 'Talabalar')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Faol'),
        ('completed', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan')
    ], default='draft')
    description = fields.Text('Izoh')

class EducationStudent(models.Model):
    _name = 'education.student'
    _description = 'Talaba'

    name = fields.Char('Ism', required=True)
    phone = fields.Char('Telefon')
    email = fields.Char('Email')
    birth_date = fields.Date('Tugʻilgan sana')
    group_id = fields.Many2one('education_group.education_group', 'Guruh')
