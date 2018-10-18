# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OpenAcademyAssistantsSelectorWzd(models.TransientModel):

    _name = "openacademy.assistants.selector.wzd"

    is_company = fields.Selection([('y', 'Yes'),('n', 'No')])
    tag_id = fields.Many2one("res.partner.category", "Tag")
    state_id = fields.Many2one("res.country.state", "Fed. State")
    assistant_ids = fields.Many2many("res.partner", string="Assistants")

    @api.multi
    def action_search(self):
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        domain = [('customer', '=', True)]
        if self.is_company:
            domain.append(('is_company', '=', self.is_company == "y"))
        if self.tag_id:
            domain.append(('category_id', 'in', [self.tag_id.id]))
        if self.state_id:
            domain.append(('state_id', '=', self.state_id.id))
        if not domain:
            raise UserError(_("Any filter set"))
        partners = partner_obj.search(domain)
        if partners:
            self.write({'assistant_ids': [(6, 0, partners.ids)]})

        return {'name': 'Assistants selector',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'openacademy.assistants.selector.wzd',
                'domain': [],
                'context': self.env.context,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
                'nodestroy': True}

    @api.multi
    def action_set_assistants(self):
        self.ensure_one()
        if not self.assistant_ids:
            raise UserError(_("Any assistants selected"))
        session = self.env["openacademy.session"].\
            browse(self.env.context['active_id'])
        session.write({'partner_ids': [(6, 0, self.assistant_ids.ids)]})
