# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Session(models.Model):

    _name = "openacademy.session"

    @api.depends('num_places', 'partner_ids')
    @api.multi
    def _get_ocupation(self):
      for session in self:
        ocupation = 0.0
        if session.num_places:
          ocupation = len(session.partner_ids) / float(session.num_places)
        session.ocupation = ocupation * 100.0

    name = fields.Char("Name", required=True)
    date = fields.Date('Date', required=True)
    duration = fields.Float('Duration', required=True)
    course_id = fields.Many2one('openacademy.course', required=True)
    responsible_id = fields.Many2one('res.users', required=True)
    num_places = fields.Integer('Num Places available', required=True)
    partner_id = fields.Many2one('res.partner', 'Teacher',
                                 domain=[('teacher', '=', True)])
    partner_ids = fields.Many2many('res.partner', 'session_partner_rel',
                                   'session_id', 'partner_id',
                                   'Assistants', required=True,
                                   domain=[('customer', '=', True)])
    ocupation = fields.Float('Ocupation', compute='_get_ocupation')


