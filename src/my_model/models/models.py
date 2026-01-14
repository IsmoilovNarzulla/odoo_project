# -*- coding: utf-8 -*-
import self

from odoo import models, fields, api


class my_model(models.Model):
    _name = 'my_model.my_model'
    _description = 'my_model.my_model'

    def test_method(self):
        print(self)           # joriy recordset
        print(self.env)       # Odoo muhiti
        print(self.env.user)  # joriy foydalanuvchi


    # res.partner modeliga murojaat qilish
    Partner = self.env['res.partner']

    # yangi mijoz yaratish
    Partner.create({'name': 'Ali Valiyev'})

    # barcha mijozlarni olish
    all_partners = Partner.search([])


    partners = self.env['res.partner'].search([('country_id.name', '=', 'Uzbekistan')])

    for partner in partners:
        print(partner.name, partner.email)



    partner = self.env['res.partner'].browse(10)
    print(partner.name)   # Ali Valiyev

    partner.write({'phone': "+998901112233"})

    records = self.env['model.name'].search(domain=[], offset=10, limit=20, order='name asc')

    # Barcha mijozlarni olish
    self.env['res.partner'].search([])

    # Faqat ismi "Ali" bo‘lgan mijozlarni olish
    self.env['res.partner'].search([('name', '=', 'Ali')])

    # Narxi 1000 dan katta bo‘lgan mahsulotlar
    self.env['product.template'].search([('list_price', '>', 1000)])

    # Birinchi 5 mijozdan keyin keladigan 5 ta mijoz
    self.env['res.partner'].search([], offset=5, limit=5)

    # Faqatgina 1 ta yozuv olish
    partner = self.env['res.partner'].search([('email', 'ilike', 'gmail')], limit=1)
    print(partner.name)

    # Ism bo‘yicha alifbo tartibida
    self.env['res.partner'].search([], order="name asc")

    # Narxi eng qimmat mahsulot
    self.env['product.template'].search([], limit=1, order="list_price desc")

    # Eng yangi yaratilgan 10 ta faktura
    self.env['account.move'].search([], limit=10, order="create_date desc")

    partners = self.env['res.partner'].search(
        domain=[('email', 'ilike', '@gmail.com')],  # faqat emailida @gmail bo‘lganlar
        offset=10,                                  # dastlabki 10 tasini tashlab ket
        limit=5,                                    # keyingi 5 ta yozuvni ol
        order="create_date desc",                   # eng oxirgi yaratilganlar
        count=False                                 # recordset qaytar
    )
    for p in partners:
        print(p.name, p.email)


    # name = fields.Char()
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()
    #
    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100

