# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubtasksFill(models.TransientModel):
    _name = 'spoc_hr_timesheet.subtask'
    _description = 'Subtasks by Projects'

    project_ids = fields.Many2many('project.project')

    def save_tasks(self):
        temp_task = self._context.get('active_id')
        temp_proj = self.env['project.task'].browse(temp_task).project_id
        for proj in self.project_ids:
            self.env['project.task'].create({'name': temp_proj.name,
                                             'display_project_id': proj.id,
                                             'parent_id': temp_task})
