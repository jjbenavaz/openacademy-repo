# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'openacademy.course'
    description = fields.Text()

    name = fields.Char(string="Title", required=True)
    _description = 'Model to store course'
