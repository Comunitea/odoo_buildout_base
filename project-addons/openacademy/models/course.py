# -*- coding: utf-8 -*-


from odoo import models, fields, api

class Course(models.Model):

    _name ="openacademy.course"

    name = fields.Char("Title", required=True)
    description = fields.Text('')

    @api.model
    def action_mi_accion(self):
        return True