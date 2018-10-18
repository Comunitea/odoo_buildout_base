# -*- coding: utf-8 -*-


from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    teacher = fields.Boolean('Is Teacher?')
