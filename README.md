# #otit.code rule wiki backend


## Developers
 - Erkka Makinen
 - Henri Koski
 - Mikko Korhonen

## Technology stack
 - Django
 - argparse
 - django-extensions
 - djangorestframework
 - psycopg2
 - six
 - wsgiref
 - PostgreSQL

## Development requirements & installation
### Requirements
- vagrant
- virtualbox

### Installation
Run 'vagrant up' and wait a while. Then 'vagrant ssh'.
Go to /vagrant/ and activate virtualenv.
Then create superuser by running pwp/manage.py createsuperuser

### Usage
With virtualenv in /vagrant activated, run /vagrant/pwp/manage.py runserver 0.0.0.0:8000
