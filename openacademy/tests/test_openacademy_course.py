from openerp.tests.common import TransactionCase
from psycopg2 import IntegrityError
from openerp.tools import mute_logger


class GlobalTestOpenAcademyCourse(TransactionCase):
    '''
    Global test to openacademy course model.
    Test create course and trigger constraints.
    '''

    # Method seudo-constructor of test setUp
    def setUp(self):
        # Define global variables to test methods
        super(GlobalTestOpenAcademyCourse, self).setUp()
        self.variable = 'hello world'
        self.course = self.env['openacademy.course']

    # Method of class that is not test
    def create_course(self, course_name, course_description,
                      course_responsible_id):
        # Create a course with given params
        self.course.create({
            'name': course_name,
            'description': course_description,
            'responsible_id': course_responsible_id
        })
        return

    # Method of test (these ones starts with 'def test_' etc)
    # Mute the error odoo.sql_db to avoid it in log
    @mute_logger('odoo.sql_db')
    def test_10_same_name_description(self):
        '''
        Test create a course with the  same name
        and description to test name different to
        description constraint
        '''
        # Expected error raised
        with self.assertRaisesRegexp(
                IntegrityError,
                'new row for relation "openacademy_course" violates check constraint "openacademy_course_name_description_check"'
                ):
            # Create a course with same name and description
            self.create_course('test', 'test', None)

    @mute_logger('odoo.sql_db')
    def test_20_two_courses_same_name(self):
        '''
        Create two courses with the
        same name to test constraint
        of unique name
        '''
        new_id = self.create_course('test1', 'test_description', None)
        print(new_id)
        with self.assertRaisesRegexp(
                IntegrityError,
                'duplicate key value violates unique constraint "openacademy_course_name_unique"'
                ):
            new_id2 = self.create_course('test1', 'test_description', None)
            print(new_id2)

    def test_30_duplicate_course(self):
        '''
        Test to duplicate a course and check that
        they work fine
        '''
        course = self.env.ref('openacademy.course0')
        course_id = course.copy()
        print(course_id)

