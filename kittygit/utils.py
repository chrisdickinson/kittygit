import os
import socket

def get_full_repo_dir(settings, user, repo):
    return os.path.expanduser(
        '/'.join([settings.get('repo_dir', '~/repos'), user, repo+'.git'])
    )

def get_clone_base_url(settings):
    login, hostname = settings.get('user', None), settings.get('host', socket.gethostname()+'.local')
    try:
        login = os.getlogin() if login is None else login
    except OSError:
        login = '<nappingcat-user>'
    return '%s@%s' % (login, hostname)

def get_full_template_dir(settings, template_dir):
    base_template_dir = os.path.expanduser(settings.get('templates_dir', '~/kittygit_templates'))
    os.path.join(
        base_template_dir, template_dir
    )
