/vagrant:
  virtualenv.managed:
    - pip_upgrade: true
    - requirements: /vagrant/requirements.txt
    - user: vagrant
