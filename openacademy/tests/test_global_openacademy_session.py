from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from psycopg2 import IntegrityError
from openerp.tools import mute_logger


class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This create global test to sessions
    '''

    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner_vauxoo = self.env.ref('base.res_partner_3')
        self.course = self.env.ref('openacademy.course1')
        self.partner_attendee = self.env.ref('base.res_partner_4')
    # generic methods


    # test methods
    def test_10_instructor_is_attendee(self):
        '''
        Check that raise of 'A session's instructor can't be an attendee'
        '''
        with self.assertRaisesRegexp(
                ValidationError,
                "A session's instructor can't be an attendee"
            ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': self.course.id,
                })

    def test_20_wkf_done(self):
        '''
        Check that the workflow works fine
        '''
        session_test = self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_attendee.id])],
                'course_id': self.course.id,
                })

    @mute_logger('odoo.sql_db')
    def test_30_session_without_course(self):
        with self.assertRaisesRegexp(
                IntegrityError,
                'null value in column "course_id" violates not-null constraint'
            ):
            sesion_test_2 = self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                })


