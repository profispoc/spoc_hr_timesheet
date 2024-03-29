# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression

class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    deal_type = fields.Selection(
        [('pay', 'To pay'),
         ('account', 'To account'),
         ('free', 'Do not bill')],
        string="Type of deal", required=True, default='free')

    contact_id = fields.Many2one("res.partner", string="Responsive contact", required=False)

    @api.onchange('partner_id')
    def _domain_change_partner_project(self):
        for line in self:
            if line.partner_id:
                return {'domain': {'project_id': [('partner_id', '=', line.partner_id.id)]}}


    @api.depends('partner_id')
    def _get_request_check(self):
        for rec in self:
            rec.is_request_check = rec.partner_id.request_check

    is_request_check = fields.Boolean(string="Is request check", compute=_get_request_check)

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    request_check = fields.Boolean(string="Requests checkout", default=False, required=True)

class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    only_user = fields.Many2one("res.users", store=True, compute="_compute_only_user")

    @api.depends('user_ids')
    def _compute_only_user(self):
        for rec in self:
            if len(rec.user_ids) != 1:
                rec.only_user = False
            else:
                rec.only_user = rec.user_ids[0]

    contact_id = fields.Many2one("res.partner", string="Responsive contact", default=False, required=False)

    @api.depends('partner_id')
    def _get_request_check(self):
        for rec in self:
            rec.is_request_check = rec.partner_id.request_check

    is_request_check = fields.Boolean(string="Is request check", default=False, compute=_get_request_check)

    @api.onchange('stage_id')
    def _scan_n_change_stage(self):
        if self.stage_id.is_closed:
            if self.project_id.ref_stage_id:
                if self.parent_id:
                    if self.parent_id.project_id:
                        temp_search = False
                        temp_next = False
                        for sid in self.parent_id.project_id.type_ids:
                            if sid == self.project_id.ref_stage_id:
                                temp_search = sid
                                continue
                            if temp_search:
                                temp_next = sid
                                temp_search = False
                        if temp_next:
                            self.parent_id.stage_id = temp_next

    @api.model
    def create(self, vals_list):
        res = super(ProjectTask, self).create(vals_list)
        if not res.parent_id:
            res.tag_ids = res.project_id.task_def_tag_ids
        else:
            res.tag_ids = res.parent_id.tag_ids
        return res

class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    ref_stage_id = fields.Many2one('project.task.type', string="Reference task stage")

    task_def_tag_ids = fields.Many2many('project.tags', string='Task default tags', relation='project_project_project_task_tag')


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.depends('analytic_line_ids.deal_type')
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()

    def _timesheet_compute_delivered_quantity_domain(self):
        domain = super(SaleOrderLine, self)._timesheet_compute_delivered_quantity_domain()
        return expression.AND([domain, [('deal_type', '=', 'pay')]])
