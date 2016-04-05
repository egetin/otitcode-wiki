run migrations:
  cmd.run:
    - user: vagrant
    - name: ". bin/activate && pwp/manage.py migrate && pwp/manage.py migrate api"
    - cwd: /vagrant
