# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubtasksFill(models.TransientModel):
    _name = 'spoc_hr_timesheet.subtask'
    _description = 'Subtasks by Projects'

    project_ids = fields.Many2many('project.project')

    def save_tasks(self):
        for proj in self.project_ids:
            print(proj.name)
