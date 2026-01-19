from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(
        string='Book Title',
        required=True,
        tracking=True
    )
    isbn = fields.Char(
        string='ISBN',
        size=13,
        tracking=True
    )
    author_id = fields.Many2one(
        'library.author',
        string='Author',
        required=True
    )
    category_id = fields.Many2one(
        'library.category',
        string='Category'
    )
    publish_date = fields.Date(
        string='Publish Date'
    )
    publisher_id = fields.Many2one(
        'library.publisher',
        string='Publisher'
    )
    pages = fields.Integer(string='Number of Pages')
    edition = fields.Char(string='Edition')
    price = fields.Float(
        string='Price',
        digits=(10, 2),
        tracking=True
    )
    cost_price = fields.Float(
        string='Cost Price',
        digits=(10, 2),
        groups='library_management.group_library_manager'
    )
    quantity = fields.Integer(
        string='Total Quantity',
        default=1
    )
    available_quantity = fields.Integer(
        string='Available Quantity',
        compute='_compute_available_quantity',
        store=True
    )
    location = fields.Char(string='Shelf Location')
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged')
    ], string='Status', default='available')

    image = fields.Binary(string='Book Cover')

    author_name = fields.Char(
        string='Author Name',
        related='author_id.name',
        store=True
    )

    borrow_ids = fields.One2many(
        'library.borrow',
        'book_id',
        string='Borrow Records'
    )

    @api.depends('quantity', 'borrow_ids', 'borrow_ids.state')
    def _compute_available_quantity(self):
        for book in self:
            borrowed_count = sum(
                borrow.quantity
                for borrow in book.borrow_ids
                if borrow.state in ['borrowed', 'reserved']
            )
            book.available_quantity = book.quantity - borrowed_count

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'ISBN must be unique!'),
        ('quantity_positive', 'CHECK(quantity >= 0)', 'Quantity must be positive!'),
    ]


    def action_mark_lost(self):
        self.write({'status': 'lost'})

    def action_mark_damaged(self):
        self.write({'status': 'damaged'})


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread']
    _rec_name = 'full_name'

    member_code = fields.Char(
        string='Member ID',
        required=True,
        default=lambda self: self._generate_member_code(),
        readonly=True
    )
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name',
        store=True
    )
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    birth_date = fields.Date(string='Birth Date')
    join_date = fields.Date(
        string='Join Date',
        default=fields.Date.today
    )
    membership_type = fields.Selection([
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('regular', 'Regular'),
        ('premium', 'Premium')
    ], string='Membership Type', default='regular')
    membership_status = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='active')


    image = fields.Binary(string='Photo')

    borrow_ids = fields.One2many(
        'library.borrow',
        'member_id',
        string='Borrowing History'
    )


    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for member in self:
            member.full_name = f"{member.first_name} {member.last_name}"


    # def _generate_member_code(self):
    #     sequence = self.env['ir.sequence'].next_by_code('library.member')
    #     return f"MEM-{sequence}"

    def _generate_member_code(self):
    # Vaqtincha oddiy usul
        last_member = self.search([], order='id desc', limit=1)
        next_id = last_member.id + 1 if last_member else 1
        return f"MEM-{next_id:04d}"

    def action_suspend(self):
        self.write({'membership_status': 'suspended'})

    def action_activate(self):
        self.write({'membership_status': 'active'})


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Book Borrowing'
    _inherit = ['mail.thread']


    name = fields.Char(
        string='Reference',
        default=lambda self: self._generate_reference(),
        readonly=True
    )
    book_id = fields.Many2one(
        'library.book',
        string='Book',
        required=True,
        domain="[('available_quantity', '>', 0)]"
    )
    member_id = fields.Many2one(
        'library.member',
        string='Member',
        required=True,
        domain="[('membership_status', '=', 'active')]"
    )
    borrow_date = fields.Date(
        string='Borrow Date',
        default=fields.Date.today
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
        default=lambda self: self._default_due_date()
    )
    return_date = fields.Date(string='Return Date')
    quantity = fields.Integer(string='Quantity', default=1)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost')
    ], string='Status', default='draft', tracking=True)


    fine_amount = fields.Float(
        string='Fine Amount',
        compute='_compute_fine_amount',
        digits=(10, 2),
        groups='library_management.group_library_accountant',
        search='_search_display_name',
    )
    fine_paid = fields.Boolean(string='Fine Paid')
    fine_payment_date = fields.Date(string='Payment Date')


    librarian_id = fields.Many2one(
        'res.users',
        string='Processed By',
        default=lambda self: self.env.user.id,
        readonly=True
    )


    @api.depends('return_date', 'due_date', 'state')
    def _compute_fine_amount(self):
        for record in self:
            if record.return_date and record.due_date and record.return_date > record.due_date:
                days_late = (record.return_date - record.due_date).days
                record.fine_amount = days_late * 1000
            else:
                record.fine_amount = 0.0


    def _generate_reference(self):
        return self.env['ir.sequence'].next_by_code('library.borrow')

    def _default_due_date(self):
        return date.today() + timedelta(days=14)


    def action_confirm(self):
        if self.book_id.available_quantity < self.quantity:
            raise UserError(_('Not enough books available!'))
        self.write({
            'state': 'borrowed',
            'borrow_date': fields.Date.today()
        })

        if self.book_id.available_quantity == self.quantity:
            self.book_id.status = 'borrowed'

    def action_return(self):
        self.write({
            'state': 'returned',
            'return_date': fields.Date.today()
        })
        if self.book_id.status == 'borrowed':
            self.book_id.status = 'available'

    def action_mark_overdue(self):
        self.write({'state': 'overdue'})

    def action_pay_fine(self):
        self.write({
            'fine_paid': True,
            'fine_payment_date': fields.Date.today()
        })


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Book Author'

    name = fields.Char(string='Author Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    nationality = fields.Char(string='Nationality')
    biography = fields.Text(string='Biography')
    book_ids = fields.One2many(
        'library.book',
        'author_id',
        string='Books'
    )


class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Book Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Category Code')
    parent_id = fields.Many2one(
        'library.category',
        string='Parent Category'
    )
    description = fields.Text(string='Description')


class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Book Publisher'

    name = fields.Char(string='Publisher Name', required=True)
    address = fields.Text(string='Address')
    contact_person = fields.Char(string='Contact Person')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')