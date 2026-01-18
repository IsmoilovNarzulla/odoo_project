from datetime import timedelta

from odoo import models, fields


class CleanupOperations(models.Model):
    _name = 'demo.cleanup'

    def delete_old_drafts(self):

        deadline = fields.Date.today() - timedelta(days=30)
        old_drafts = self.env['sale.order'].search([
            ('create_date', '<', deadline),
            ('state', '=', 'draft')
        ])

        deleted_count = 0
        for order in old_drafts:
            if order.invoice_ids:
                continue
            order.unlink()
            deleted_count += 1

        return {
            'warning': {
                'title': 'Oʻchirish natijasi',
                'message': f'{deleted_count} ta qoralama buyurtma o‘chirildi'
            }
        }

    def safe_delete(self):
        backup_data = []

        for record in self:
            backup_data.append({
                'id': record.id,
                'name': record.name,
                'data': record.read()[0]
            })
            if hasattr(record, 'line_ids'):
                record.line_ids.unlink()
            record.unlink()

        if backup_data:
            self.env['deleted.data.backup'].create({
                'model_name': self._name,
                'backup_data': str(backup_data),
                'deleted_by': self.env.user.id,
            })