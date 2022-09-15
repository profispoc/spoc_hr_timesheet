# -*- coding: utf-8 -*-

from odoo import models, fields, api


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

    def timesheet_project_reinit(self):
        ts = self.env['account.analytic.line'].browse(self.id)
        is_task_cond = False
        is_tag_cond =  False
        is_proj_cond = False

        if ts.task_id:
            if ts.task_id.parent_id:
                if ts.task_id.parent_id.project_id:
                    is_task_cond = True

        if is_task_cond:
            for tag in ts.task_id.project_id.tag_ids:
                if tag.name == 'технічний проект':
                    is_tag_cond = True

        if is_tag_cond:
            if ts.project_id == ts.task_id.project_id:
                is_proj_cond = True

        if is_proj_cond:
            ts.write({'project_id': ts.task_id.parent_id.project_id.id})

    def timesheet_name_prefix(self):
        ts = self.env['account.analytic.line'].browse(self.id)
        is_task_cond = False
        is_tag_cond =  False
        is_proj_cond = False

        if ts.task_id:
            if ts.task_id.parent_id:
                if ts.task_id.parent_id.project_id:
                    is_task_cond = True

        if is_task_cond:
            for tag in ts.task_id.project_id.tag_ids:
                if tag.name == 'технічний проект':
                    is_tag_cond = True

        if is_tag_cond:
            if ts.project_id != ts.task_id.project_id:
                is_proj_cond = True

        if is_proj_cond:
            tech_project_name = ts.task_id.project_id.name
            ts_name = ts.name
            if ts.name[0:len(tech_project_name)] != tech_project_name:
                ts.write({'name': tech_project_name+"@"+ts_name})

    @api.model
    def create(self, vals_list):
        res = super(AccountAnalyticLine, self).create(vals_list)
        self.timesheet_project_reinit()
        self.timesheet_name_prefix()
        return res

    def write(self, vals):
        res = super(AccountAnalyticLine, self).write(vals)
        self.timesheet_project_reinit()
        self.timesheet_name_prefix()
        return res


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    request_check = fields.Boolean(string="Requests checkout", default=False, required=True)

class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

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
