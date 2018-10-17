# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Course(models.Model):

    _name = "openacademy.course"

    name = fields.Char("Title", required=True)
    description = fields.Text('')
    dificulty = fields.Selection([('easy', 'Easy'),
                                  ('medium', 'Medium'),
                                  ('hard', 'Hard')], 'Dificulty',
                                 default='medium')
    type_id = fields.Many2one('openacademy.course.type', 'Type', required=True)
    responsible_id = fields.Many2one('res.users', 'Responsible', required=True)
    session_ids = fields.One2many('openacademy.session', 'course_id')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique")
    ]

    @api.multi
    def action_mi_action(self):
        self.ensure_one()
        return True

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + '_copy'
        return super(Course, self).copy(default)
