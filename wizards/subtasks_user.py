# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubtasksFillUserLine(models.TransientModel):
    _name = 'subtaskuser.line'
    _description = 'Subtasks by Users line'

    subtaskuser_id = fields.Many2one('subtaskuser')
    user_id = fields.Many2one('res.users', string="Authorized")
    to_subtask = fields.Boolean("To subtask")

class SubtasksFillUser(models.TransientModel):
    _name = 'subtaskuser'
    _description = 'Subtasks by Users'

    subtaskuser_line_ids = fields.One2many('subtaskuser.line', 'subtaskuser_id', string="Authorized")

    def default_get(self, fields):
        res = super().default_get(fields)
        subtask_ids = self._context.get('child_ids')
        used_users = []
        for subtask_id in subtask_ids:
            subtask = self.env['project.task'].browse(subtask_id[1])
            for subuser in subtask.user_ids:
                used_users.append(subuser.id)
        res['subtaskuser_line_ids'] = [
            (0, 0, {'to_subtask': False if task_user_id in used_users else True,
                    'user_id': task_user_id})
            for task_user_id in self._context.get('user_ids')[0][2]
        ]
        return res

    def save_tasks(self):
        temp_task = self.env['project.task'].browse(self._context.get('active_id'))
        temp_proj = temp_task.project_id
        for user_line in self.subtaskuser_line_ids:
            if user_line.to_subtask:
                self.env['project.task'].create({'name': temp_task.name,
                                                 'display_project_id': temp_proj.id,
                                                 'parent_id': temp_task.id,
                                                 'user_ids': [user_line.user_id.id]})
