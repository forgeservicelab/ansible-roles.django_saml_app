"""
Django settings for samldemo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import logging
logging.basicConfig(level=logging.DEBUG)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@!poms#fy-w!ad&i945blb)arnx!(zj$37x1b$n9l_8*$2=m-0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosaml2',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'samldemo.urls'

WSGI_APPLICATION = 'samldemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
)

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


import saml2
SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': '{{ ansible_fqdn }}/saml2/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': '/usr/local/lib/python2.7/dist-packages/saml2/attributemaps',

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'allow_unsolicited': True,
          'name': 'Federated Django sample SP',
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ('http://{{ ansible_fqdn }}/saml2/acs/',
                   saml2.BINDING_HTTP_POST),
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ('http://{{ ansible_fqdn }}/saml2/ls/',
                   saml2.BINDING_HTTP_REDIRECT),
                  ],
              },

           # attributes that this project need to identify a user
          'required_attributes': ['cn'],

           # attributes that may be useful to have but not required
          'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          'idp': {
              # we do not need a WAYF service since there is
              # only an IdP defined here. This IdP should be
              # present in our metadata

              # the keys of this dictionary are entity ids
              '{{ django_saml_app_idp }}/saml2/idp/metadata.php': {
                  'single_sign_on_service': {
                      saml2.BINDING_HTTP_REDIRECT: '{{ django_saml_app_idp }}/saml2/idp/SSOService.php',
                      },
                  'single_logout_service': {
                      saml2.BINDING_HTTP_REDIRECT: '{{ django_saml_app_idp }}/saml2/idp/SingleLogoutService.php',
                      },
                  },
              },
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [os.path.join(BASE_DIR, 'remote_metadata.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': os.path.join(BASE_DIR, 'key'),
  'cert_file': os.path.join(BASE_DIR, 'cert.crt'),

  # own metadata settings
  'contact_person': [
      {'given_name': 'Tomas',
       'sur_name': 'Karasek',
       'company': 'Digile',
       'email_address': 'tomas.karasek@digile.fi',
       'contact_type': 'technical'},
      {'given_name': 'Tomas',
       'sur_name': 'Karasek',
       'company': 'Digile',
       'email_address': 'tomas.karasek@digile.fi',
       'contact_type': 'administrative'},
      ],
  # you can set multilanguage information here
  'organization': {
      'name': [('Digile', 'en')],
      'display_name': [('Digile', 'en')],
      'url': [('http://forgeservicelab.fi', 'en')],
      },
  'valid_for': 24,  # how long is our metadata valid
  }

SAML_ATTRIBUTE_MAPPING = {
# cn is in the OID notation urn:oid:2.5.4.3
    'cn': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', )
}