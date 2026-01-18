# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contactexport_wizard(models.Model):
    _name = 'contactexport_wizard.contactexport_wizard'
    _description = 'Kontaktlarni eksport qilish wizard'

    export_format = fields.Selection([
        ('csv', 'CSV fayl'),
        ('excel', 'Excel fayl'),
        ('pdf', 'PDF hisobot')
    ], string='Eksport formati', default='csv')

    include_phone = fields.Boolean(string='Telefon raqamini kiritish', default=True)
    include_email = fields.Boolean(string='Emailni kiritish', default=True)
    include_address = fields.Boolean(string='Manzilni kiritish', default=True)
    export_result = fields.Text(string='Eksport natijasi', readonly=True)
    export_file = fields.Binary(string='Eksport fayli', readonly=True)
    filename = fields.Char(string='Fayl nomi')

    def action_export(self):
        active_ids = self.env.context.get('active_ids', [])
        contacts = self.env['res.partner'].browse(active_ids)
        export_data = []
        for contact in contacts:
            row = {'name': contact.name}
            if self.include_phone:
                row['phone'] = contact.phone or ''
            if self.include_email:
                row['email'] = contact.email or ''
            if self.include_address:
                row['address'] = contact.street or ''

            export_data.append(row)
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
        writer.writeheader()
        writer.writerows(export_data)
        self.write({
            'export_result': f"{len(contacts)} ta kontakt eksport qilindi",
            'export_file': output.getvalue().encode(),
            'filename': f'contacts_export_{fields.Date.today()}.csv'
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

