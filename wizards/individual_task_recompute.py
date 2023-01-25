# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IndividualRecompute(models.TransientModel):
    _name = 'individual.recompute'
    _description = 'Individual Task Recompute'

    def proceed(self):
        all_tasks = self.env['project.task'].search([])
        for task in all_tasks:
            if len(task.user_ids) != 1:
                task.write({'only_user': False})
            else:
                task.write({'only_user': task.user_ids[0]})
