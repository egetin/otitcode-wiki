postgresql repository:
  pkgrepo.managed:
    - humanname: PostgreSQL repository
    - name: deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
    - file: /etc/apt/sources.list.d/pgdg.list

get pg repository key:
  cmd.run:
    - name: wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

update repositories:
  cmd.run:
    - name: apt-get update

postgresql-9.5:
  pkg.installed

postgresql-server-dev-9.5:
  pkg.installed

postgresql:
  service:
    - running
    - enable: true
    - watch:
      - file: /etc/postgresql/9.5/main/pg_hba.conf

devuser:
  postgres_user.present:
    - password: password
    - user: postgres

wiki_development:
  postgres_database.present:
    - encoding: UTF8
    - template: template0
    - owner: devuser
    - user: postgres

/etc/postgresql/9.5/main/pg_hba.conf:
  file.managed:
    - source: salt://files/pg_hba.conf
