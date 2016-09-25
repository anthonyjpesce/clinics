from fabric.operations import put
from fabric.api import env, task

@task
def copy_settings():
    put('/home/anthony/code/personal/clinics/repo/project/settings_private.py', '/apps/clinics/repo/project/settings_private.py', use_sudo=True)

