# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubtasksFillUser(models.TransientModel):
    _name = 'spoc_hr_timesheet.subtaskuser'
    _description = 'Subtasks by Users'

    def default_user_ids(self):
        return self._context.get('user_ids')

    user_ids = fields.Many2many('res.users', string="Authorized", default=default_user_ids)

    def save_tasks(self):
        temp_task = self.env['project.task'].browse(self._context.get('active_id'))
        temp_proj = temp_task.project_id
        for user in self.user_ids:
            self.env['project.task'].create({'name': temp_task.name,
                                                 'display_project_id': temp_proj.id,
                                                 'parent_id': temp_task.id,
                                                 'user_ids': [user.id]})
