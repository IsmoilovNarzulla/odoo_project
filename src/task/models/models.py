# -*- coding: utf-8 -*-

from odoo import models, fields, api


class task(models.Model):
    _name = "task.task"
    _description = 'Task'
    _order = "priority desc, id desc"

    name = fields.Char("Task Name", required=True)
    description = fields.Text("Task description")
    stage_id = fields.Many2one("uic.task.stage", required=True,group_expand='_read_group_stage_id')
    plan_hours = fields.Float(string="Planning Hours", default=1)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('done', 'Done'),
    ],default='draft')

    priority = fields.Selection([
        ("0", "Low"),
        ("1", "Medium"),
        ("2", "High"),
        ("3", "Critical"),
        ("4", "Very High"),
    ], default="0")

    status = fields.Selection([
        ("not_started", "Not Started"),
        ("started", "Started"),
        ("finished", "Finished"),
    ], default="not_started")

    @api.model
    def _read_group_stage_id(self, records, domain):
        return self.env["uic.task.stage"].search([])


class taskstage(models.Model):
    _name = "uic.task.stage"
    _description = "Task stage"

    name = fields.Char(string="Stage Name", required=True)
