from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    # _inherit = 'res.partner'

    mobile = fields.Char(string="Mobil Telefon")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            phone = vals.get('phone', '') or vals.get('mobile', '')
            if phone:
                phone = str(phone).strip()
                if not phone.startswith('+998'):
                    if phone.startswith('998'):
                        phone = '+' + phone
                    elif phone.startswith('0'):
                        phone = '+998' + phone[1:]
                    else:
                        phone = '+998' + phone
                vals['phone'] = phone

        return super(ResPartner, self).create(vals_list)


class ResPartner2(models.Model):
    _inherit = 'res.partner'

    def write(self, vals, _logger=None):
        if 'phone' in vals:
            phone = vals['phone']
            if phone:
                phone = str(phone).strip()
                if not phone.startswith('+998'):
                    if phone.startswith('998'):
                        phone = '+' + phone
                    elif phone.startswith('0'):
                        phone = '+998' + phone[1:]
                    else:
                        phone = '+998' + phone
                vals['phone'] = phone


        if 'mobile' in vals:
            mobile = vals['mobile']
            if mobile:
                mobile = str(mobile).strip()
                if not mobile.startswith('+998'):
                    if mobile.startswith('998'):
                        mobile = '+' + mobile
                    elif mobile.startswith('0'):
                        mobile = '+998' + mobile[1:]
                    else:
                        mobile = '+998' + mobile
                vals['mobile'] = mobile


        result = super(ResPartner, self).write(vals)


        for partner in self:
            _logger.info(f"Mijoz yangilandi: {partner.name}")

        return result


class ResPartner3(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        if 'email' in vals and vals['email']:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, vals['email']):
                raise ValidationError("Noto'g'ri email formati!")

        return super(ResPartner, self).write(vals)