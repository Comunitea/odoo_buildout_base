# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Session(models.Model):

    _name = "openacademy.session"

    @api.depends('num_places', 'partner_ids')
    @api.multi
    def _get_ocupation(self):
        for session in self:
            oc = 0.0
            if session.num_places:
                oc = len(session.partner_ids) / float(session.num_places)
        session.ocupation = oc * 100.0

    name = fields.Char("Name", required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today())
    duration = fields.Float('Duration', required=True)
    course_id = fields.Many2one('openacademy.course', required=True)
    responsible_id = fields.Many2one('res.users', required=True)
    num_places = fields.Integer('Num Places available', required=True)
    partner_id = fields.Many2one('res.partner', 'Teacher',
                                 domain=[('teacher', '=', True)])
    partner_ids = fields.Many2many('res.partner', 'session_partner_rel',
                                   'session_id', 'partner_id',
                                   'Assistants', required=True,
                                   domain=[('customer', '=', True)],
                                   copy=False)
    ocupation = fields.Float('Ocupation', compute='_get_ocupation')
    active = fields.Boolean('Active', default=True)

    @api.onchange('num_places', 'partner_ids')
    def ochange_num_places_assistants(self):
        res = {}
        msg = ''
        if self.num_places < 0:
            msg = _('Num places can not be negative')
        if len(self.partner_ids) > self.num_places:
            msg = _('Not enought free places')
        if msg:
            res = {
                'warning': {
                    'title': "Warning!",
                    'message': msg,
                }
            }
        return res

    @api.constrains('num_places')
    def _check_num_places(self):
        for session in self:
            if session.num_places < 0:
                raise ValidationError(_('Num places can not be negative'))

    @api.constrains('partner_id')
    def _check_partner_id(self):
        for session in self:
            if session.partner_id.id in session.partner_ids.ids:
                raise ValidationError(
                    _('Partner %s can not be in assistants' % session.partner_id.name))
