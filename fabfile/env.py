from fabric.api import env
from os.path import expanduser

env.key_filename = (expanduser("~/.ec2/tstd.today.pem"),)
env.user = 'ubuntu'
env.known_hosts = "/tmp/tmp_known_hosts_ec2"
env.chef = '/usr/local/bin/chef-solo -c solo.rb -j node.json'
env.app_user = 'anthony'
env.project_dir = '/apps/clinics/repo/'
env.activate = "source /apps/clinics/bin/activate"
env.branch = 'master'
env.AWS_SECRET_ACCESS_KEY = ''
env.AWS_ACCESS_KEY_ID = ''

def prod():
    env.hosts = ("tstd.today",)