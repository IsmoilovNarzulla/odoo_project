# models/library_rules.py
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class LibraryCustomRules(models.Model):
    _name = 'library.rules'
    _description = 'Library Business Rules'

    name = fields.Char(string='Rule Name', required=True)
    rule_type = fields.Selection([
        ('borrow_limit', 'Borrowing Limit'),
        ('fine_calculation', 'Fine Calculation'),
        ('membership', 'Membership Rules'),
        ('book', 'Book Rules'),
        ('other', 'Other')
    ], string='Rule Type', required=True)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')


    max_books_per_member = fields.Integer(
        string='Max Books per Member',
        default=3,
        help='Maximum number of books a member can borrow at once'
    )
    borrow_duration_days = fields.Integer(
        string='Borrow Duration (days)',
        default=14,
        help='Default number of days for borrowing'
    )
    max_renewals = fields.Integer(
        string='Maximum Renewals',
        default=2,
        help='Maximum number of times a book can be renewed'
    )


    fine_per_day = fields.Float(
        string='Fine per Day',
        default=1000.0,
        help='Fine amount per day for late return'
    )
    grace_period_days = fields.Integer(
        string='Grace Period (days)',
        default=3,
        help='Number of grace days before fine starts'
    )
    max_fine_amount = fields.Float(
        string='Maximum Fine Amount',
        default=50000.0,
        help='Maximum fine amount that can be charged'
    )


    student_membership_fee = fields.Float(
        string='Student Membership Fee',
        default=50000.0
    )
    teacher_membership_fee = fields.Float(
        string='Teacher Membership Fee',
        default=75000.0
    )
    regular_membership_fee = fields.Float(
        string='Regular Membership Fee',
        default=100000.0
    )
    premium_membership_fee = fields.Float(
        string='Premium Membership Fee',
        default=150000.0
    )
    membership_duration_months = fields.Integer(
        string='Membership Duration (months)',
        default=12
    )


    minimum_book_quantity = fields.Integer(
        string='Minimum Book Quantity',
        default=1,
        help='Minimum quantity of books that must be in stock'
    )
    reservation_duration_days = fields.Integer(
        string='Reservation Duration (days)',
        default=7,
        help='How long a book can be reserved'
    )


    domain_filter = fields.Char(
        string='Domain Filter',
        help='Apply this rule only to records matching this domain'
    )


    sequence = fields.Integer(string='Sequence', default=10)

    @api.model
    def get_active_rule(self, rule_type):
        return self.search([
            ('rule_type', '=', rule_type),
            ('active', '=', True)
        ], order='sequence', limit=1)

    def validate_member_borrow_limit(self, member_id, book_quantity=1):
        rule = self.get_active_rule('borrow_limit')
        if not rule:
            return True

        Borrow = self.env['library.borrow']
        current_borrows = Borrow.search_count([
            ('member_id', '=', member_id),
            ('state', 'in', ['borrowed'])
        ])

        total_after = current_borrows + book_quantity
        if total_after > rule.max_books_per_member:
            raise UserError(_(
                'Borrowing limit exceeded! %s books currently borrowed/reserved. '
                'Maximum allowed is %s books.'
            ) % (current_borrows, rule.max_books_per_member))
        return True

    def calculate_fine_amount(self, due_date, return_date):
        rule = self.get_active_rule('fine_calculation')
        if not rule:
            return 0.0

        if not due_date or not return_date:
            return 0.0

        due = fields.Date.from_string(due_date)
        ret = fields.Date.from_string(return_date)

        if ret <= due:
            return 0.0

        days_late = (ret - due).days
        days_after_grace = max(0, days_late - rule.grace_period_days)

        fine = days_after_grace * rule.fine_per_day
        return min(fine, rule.max_fine_amount)

    def get_membership_fee(self, membership_type):
        rule = self.get_active_rule('membership')
        if not rule:
            return 0.0

        fees = {
            'student': rule.student_membership_fee,
            'teacher': rule.teacher_membership_fee,
            'regular': rule.regular_membership_fee,
            'premium': rule.premium_membership_fee,
        }
        return fees.get(membership_type, 0.0)

    def check_book_availability(self, book_id, quantity=1):
        rule = self.get_active_rule('book')
        if not rule:
            return True

        book = self.env['library.book'].browse(book_id)
        if book.quantity < rule.minimum_book_quantity:
            raise UserError(_(
                'Book quantity is below minimum required! '
                'Current: %s, Minimum: %s'
            ) % (book.quantity, rule.minimum_book_quantity))


        if book.available_quantity < quantity:
            raise UserError(_(
                'Not enough books available! '
                'Requested: %s, Available: %s'
            ) % (quantity, book.available_quantity))

        return True

    def validate_book_price(self, price, cost_price):
        if price <= 0:
            raise ValidationError(_('Price must be greater than 0!'))

        if cost_price and price < cost_price:
            raise ValidationError(_(
                'Selling price cannot be lower than cost price! '
                'Cost: %s, Selling: %s'
            ) % (cost_price, price))

        return True

    @api.model
    def apply_rules_to_borrow(self, borrow_vals):
        member_id = borrow_vals.get('member_id')
        book_id = borrow_vals.get('book_id')
        quantity = borrow_vals.get('quantity', 1)
        self.validate_member_borrow_limit(member_id, quantity)
        self.check_book_availability(book_id, quantity)
        rule = self.get_active_rule('borrow_limit')
        if rule and 'due_date' not in borrow_vals:
            from datetime import date, timedelta
            borrow_date = borrow_vals.get('borrow_date', date.today())
            if isinstance(borrow_date, str):
                borrow_date = fields.Date.from_string(borrow_date)
            due_date = borrow_date + timedelta(days=rule.borrow_duration_days)
            borrow_vals['due_date'] = fields.Date.to_string(due_date)

        return borrow_vals


class LibraryBorrow(models.Model):
    _inherit = 'library.borrow'

    renewal_count = fields.Integer(
        string='Renewal Count',
        default=0,
        readonly=True
    )

    @api.constrains('member_id', 'book_id', 'quantity')
    def _check_borrow_rules(self):
        Rules = self.env['library.rules']
        for record in self:
            if record.state in ['draft', 'borrowed']:
                Rules.validate_member_borrow_limit(
                    record.member_id.id,
                    record.quantity
                )
                Rules.check_book_availability(
                    record.book_id.id,
                    record.quantity
                )

    def action_renew(self):
        self.ensure_one()

        Rules = self.env['library.rules']
        rule = Rules.get_active_rule('borrow_limit')

        if not rule:
            raise UserError(_('No active borrowing rules found!'))
        if self.renewal_count >= rule.max_renewals:
            raise UserError(_(
                'Maximum renewals reached! '
                'Current: %s, Maximum: %s'
            ) % (self.renewal_count, rule.max_renewals))
        from datetime import timedelta
        current_due = fields.Date.from_string(self.due_date)
        new_due = current_due + timedelta(days=rule.borrow_duration_days)

        self.write({
            'due_date': fields.Date.to_string(new_due),
            'renewal_count': self.renewal_count + 1
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrow',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }


class LibraryMember(models.Model):
    _inherit = 'library.member'

    membership_expiry_date = fields.Date(
        string='Membership Expiry Date',
        compute='_compute_membership_expiry',
        store=True
    )
    membership_fee_paid = fields.Boolean(
        string='Membership Fee Paid',
        default=False
    )

    @api.depends('join_date')
    def _compute_membership_expiry(self):
        Rules = self.env['library.rules']
        rule = Rules.get_active_rule('membership')

        for member in self:
            if member.join_date and rule:
                from datetime import timedelta
                join_date = fields.Date.from_string(member.join_date)
                expiry_date = join_date + timedelta(days=rule.membership_duration_months * 30)
                member.membership_expiry_date = fields.Date.to_string(expiry_date)
            else:
                member.membership_expiry_date = False

    def check_membership_validity(self):
        for member in self:
            if member.membership_expiry_date:
                today = fields.Date.today()
                expiry = fields.Date.from_string(member.membership_expiry_date)

                if today > expiry:
                    member.membership_status = 'expired'
                    return False
            return True

    @api.constrains('membership_type')
    def _check_membership_fee(self):
        for member in self:
            if not member.membership_fee_paid:
                Rules = self.env['library.rules']
                fee = Rules.get_membership_fee(member.membership_type)

                if fee > 0:
                    raise ValidationError(_(
                        'Membership fee must be paid for %s membership! '
                        'Required amount: %s'
                    ) % (member.membership_type, fee))


class LibraryBook(models.Model):
    _inherit = 'library.book'

    @api.constrains('price', 'cost_price')
    def _check_price_rules(self):
        Rules = self.env['library.rules']
        for book in self:
            Rules.validate_book_price(book.price, book.cost_price)

_logger = logging.getLogger(__name__)
class LibraryRuleEnforcer(models.AbstractModel):
    _name = 'library.rule.enforcer'
    _description = 'Library Rule Enforcer'

    def _enforce_rules(self, record, rule_type):
        Rules = self.env['library.rules']
        active_rules = Rules.search([
            ('rule_type', '=', rule_type),
            ('active', '=', True),
            ('domain_filter', '!=', False)
        ], order='sequence')

        for rule in active_rules:
            try:
                domain = eval(rule.domain_filter, {
                    'record': record,
                    'env': self.env,
                    'context': self._context
                })

                if domain:
                    if self._check_domain(record, domain):
                        self._apply_rule(record, rule)
            except Exception as e:
                _logger.error("Error applying rule %s: %s", rule.name, str(e))

    def _check_domain(self, record, domain):
        return True





def check_rules_on_borrow(borrow):
    Rules = borrow.env['library.rules']
    Rules.validate_member_borrow_limit(
        borrow.member_id.id,
        borrow.quantity
    )


    Rules.check_book_availability(
        borrow.book_id.id,
        borrow.quantity
    )


    if borrow.state == 'returned' and borrow.return_date and borrow.due_date:
        fine = Rules.calculate_fine_amount(
            borrow.due_date,
            borrow.return_date
        )
        if fine > 0:
            borrow.fine_amount = fine



RULES_DEMO_DATA = [
    {
        'name': 'Standard Borrowing Rules',
        'rule_type': 'borrow_limit',
        'max_books_per_member': 3,
        'borrow_duration_days': 14,
        'max_renewals': 2,
        'description': 'Standard borrowing rules for all members'
    },
    {
        'name': 'Fine Calculation Rules',
        'rule_type': 'fine_calculation',
        'fine_per_day': 1000.0,
        'grace_period_days': 3,
        'max_fine_amount': 50000.0,
        'description': 'Rules for calculating late return fines'
    },
    {
        'name': 'Membership Fee Rules',
        'rule_type': 'membership',
        'student_membership_fee': 50000.0,
        'teacher_membership_fee': 75000.0,
        'regular_membership_fee': 100000.0,
        'premium_membership_fee': 150000.0,
        'membership_duration_months': 12,
        'description': 'Membership fees for different member types'
    },
    {
        'name': 'Book Management Rules',
        'rule_type': 'book',
        'minimum_book_quantity': 1,
        'reservation_duration_days': 7,
        'description': 'Rules for book inventory management'
    }
]

