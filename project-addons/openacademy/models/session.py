# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Session(models.Model):

    _name = "openacademy.session"
    _inherit = ["mail.thread"]

    @api.depends('num_places', 'partner_ids')
    @api.multi
    def _get_ocupation(self):
        for session in self:
            oc = 0.0
            if session.num_places:
                oc = len(session.partner_ids) / float(session.num_places)
        session.ocupation = oc * 100.0

    name = fields.Char("Name", required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    duration = fields.Float('Duration', required=True)
    course_id = fields.Many2one('openacademy.course', required=True)
    responsible_id = fields.Many2one('res.users', required=True)
    num_places = fields.Integer('Num Places available', required=True,
                                track_visibility="onchange")
    professor_id = fields.Many2one('res.users', 'Teacher',
                                   domain=[('teacher', '=', True)],
                                   default=lambda self: self.env.user)
    partner_ids = fields.Many2many('res.partner', 'session_partner_rel',
                                   'session_id', 'partner_id',
                                   'Assistants', required=True,
                                   domain=[('customer', '=', True)],
                                   copy=False)
    ocupation = fields.Float('Ocupation', compute='_get_ocupation')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('preparation', 'In preparation'),
         ('open', 'Open registration'),
         ('completed', 'Completed'), ('cancel', 'cancel')],
        default='preparation')

    def action_open(self):
        """
            Cambiamos de preparation a open
        """
        self.write({'state': 'open'})

    def action_complete(self):
        """
            Cambiamos de open a completed
        """
        self.write({'state': 'completed'})

    def action_cancel(self):
        """
            Cambiamos de completed a cancel
        """
        if self.state == 'completed':
            raise UserError(_('cannot cancel a completed session'))
        self.write({'state': 'cancel'})

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

    @api.constrains('professor_id', 'partner_ids')
    def _check_partner_id(self):
        for session in self:
            if session.professor_id.partner_id in session.partner_ids:
                raise ValidationError(
                    _('Partner %s can not be in assistants') %
                    session.professor_id.name)

    @api.multi
    def unlink(self):
        for session in self:
            if session.state in ('open', 'completed'):
                raise UserError(_("Cannot delete sessions in open or "
                                  "completed state"))
        return super(Session, self).unlink()
