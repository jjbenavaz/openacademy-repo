from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many(
        'openacademy.session', string="Attended Sessions",
        readonly=True)
