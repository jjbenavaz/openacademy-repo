import functools
import xmlrpc.client


HOST = 'localhost'
PORT = 8069
DB = 'odoodb'
USER = 'John Smith'
PASS = '1234'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print ("Logged in as %s (uid:%d)" % (USER,uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
sessions = call('openacademy.session','search_read', [], ['name','seats', 'course_id'])
for session in sessions:
    print ("Session %s (%s seats) %s" % (session['name'], session['seats'], session['course_id']))
# 3.create a new session
course_id = call('openacademy.course', 'search', [('name','ilike','Curso')])[0]

session_id = call('openacademy.session', 'create', {
    'name' : 'My session assigned 2',
    'course_id' : course_id,
    })

