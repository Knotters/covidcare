import environ
env = environ.Env()
environ.Env.read_env()

PROJECTKEY = env('PROJECTKEY')
PUBNAME = env('PUBNAME')
ENV = env('ENV')
HOSTS = env('HOSTS').split(',')
DBNAME = env('DBNAME')
DBLINK = env('DBLINK')
DBUSER = env('DBUSER')
DBPASS = env('DBPASS')

MAILUSER = env('MAILUSER')
MAILPASS = env('MAILPASS')
ADMINPATH = env('ADMINPATH')
SUPERDOMAIN = env('SUPERDOMAIN')
GOOGLE_CRED = env('googleCred')
SPREADSHEETID = env('worksheetId')
SITE = env('SITE')

ISPRODUCTION = ENV == 'production'