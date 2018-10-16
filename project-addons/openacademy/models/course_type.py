# -*- coding: utf-8 -*-


from odoo import models, fields

class CourseType(models.Model):

    _name ="openacademy.course.type"

    code     = fields.Char("Title", required=True)
    description = fields.Text('', required=True)
