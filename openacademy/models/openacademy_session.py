from odoo import models, fields, api, exceptions
from datetime import timedelta
import time


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Model to manage and schedule course sessions'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    datetime_test = fields.Datetime(default=fields.Datetime.now)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one(
            'res.partner',
            domain=['|', ('instructor', '=', True),
            ('category_id.name', 'ilike', 'Teacher')])
    course_id = fields.Many2one(
            'openacademy.course',
            ondelete='cascade',
            required=True)
    attendee_ids = fields.Many2many('res.partner')
    taken_seats = fields.Float(compute='_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(
            compute='_get_end_date',
            inverse='_set_end_date', store=True)
    attendees_count =  fields.Integer(compute='_get_attendees_count', store=True)
    color = fields.Integer()

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendee_ids)

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for record in self.filtered('start_date'):
            start_date = fields.Datetime.from_string(record.start_date)
            record.end_date = start_date + timedelta(days=record.duration, seconds=-1)

    def _set_end_date(self):
        for record in self.filtered('start_date'):
            start_date = fields.Datetime.from_string(record.start_date)
            end_date = fields.Datetime.from_string(record.end_date)
            record.duration = (end_date - start_date).days + 1

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            self.active = False
            return {
                    'warning': {
                        'title': "Incorrect 'seats' value",
                        'message': "The number of available seats may not be negative",
                        }
                    }
        if self.seats < len(self.attendee_ids):
            self.active = False
            return {
                    'warning': {
                        'title': "Too many attendees",
                        'message': "Increase seats or remove excess attendees",
                        }
                    }
        self.active = True

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self.filtered('instructor_id'):
            if record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError(
                        "A session's instructor can't be an attendee"
                        )
