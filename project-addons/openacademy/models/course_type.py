# -*- coding: utf-8 -*-


from odoo import models, fields


class CourseType(models.Model):

    _name = "openacademy.course.type"
    _rec_name = ''

    name = fields.Char("Name", required=True)
    code = fields.Char("Title", required=True)
    description = fields.Text('', required=True)
