from odoo import models, api


class AuditMixin(models.AbstractModel):
    _name = 'audit.mixin'
    _description = 'Audit Trail Mixin'

    def _log_operation(self, operation_type, vals=None, old_vals=None):
        log_model = self.env['operation.log']
        for record in self:
            log_model.create({
                'name': f"{record._name} - {operation_type}",
                'model_name': record._name,
                'record_id': record.id,
                'record_name': record.display_name or str(record.id),
                'operation_type': operation_type,
                'user_id': self.env.user.id,
                'old_values': str(old_vals) if old_vals else '',
                'new_values': str(vals) if vals else '',
                'ip_address': self.env.request.httprequest.remote_addr
                if hasattr(self.env, 'request') and self.env.request else ''
            })

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AuditMixin, self).create(vals_list)
        for i, record in enumerate(records):
            record._log_operation('create', vals=vals_list[i])
        return records

    def write(self, vals):
        old_values = {}
        for record in self:
            old_values[record.id] = {
                field: getattr(record, field)
                for field in vals.keys()
                if hasattr(record, field)
            }
        result = super(AuditMixin, self).write(vals)
        for record in self:
            record._log_operation('write', vals=vals, old_vals=old_values.get(record.id))
        return result


    def unlink(self):
        for record in self:
            record._log_operation('unlink', old_vals={
                field.name: getattr(record, field.name)
                for field in record._fields.values()
                if not field.computed
            })
        return super(AuditMixin, self).unlink()