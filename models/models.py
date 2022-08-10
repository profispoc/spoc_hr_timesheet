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