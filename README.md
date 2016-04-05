# #otit.code rule wiki

## Developers
 - Erkka Makinen
 - Henri Koski
 - Mikko Korhonen

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
