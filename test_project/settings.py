INSTALLED_APPS = ['exchange',
                  'south']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db'
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

OPENEXCHANGERATES_API_KEY = '<DUMMY_KEY>'
SECRET_KEY = 'dummy_secret_key'