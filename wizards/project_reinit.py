# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectReinit(models.TransientModel):
    _name = 'spoc_hr_timesheet.project_reinit'

    def default_filter_date_start(self):
        return fields.Date.start_of(fields.Date.today(), 'month')

    def default_filter_date_stop(self):
        return fields.Date.end_of(fields.Date.today(), 'month')

    def default_timesheets(self):
        timesheets = self.env['account.analytic.line'].search([('date', '>=', self.filter_date_start),
                                                               ('date', '<=', self.filter_date_stop)])
        recs = []
        for ts in timesheets:
            is_check = False
            for tag in ts.task_id.project_id.tag_ids:
                if tag.is_tech:
                    if ts.project_id == ts.task_id.project_id:
                        is_check = True
            if is_check:
                if ts.task_id.parent_id:
                    if ts.task_id.parent_id.project_id:
                        recs.append(ts.id)
        return recs

    filter_date_start = fields.Date(default=default_filter_date_start)
    filter_date_stop = fields.Date(default=default_filter_date_stop)
    timesheets = fields.Many2many('account.analytic.line', default=default_timesheets)

    def save_timesheets(self):
        for ts in self.timesheets:
            ts.project_id = ts.task_id.parent_id.project_id

    @api.onchange('filter_date_start', 'filter_date_stop')
    def change_filter(self):
        self.timesheets = False
        self.timesheets = self.default_timesheets()
