from nappingcat import auth
from nappingcat.exceptions import NappingCatRejected
import os
import subprocess
import sys

def get_settings(request):
    return dict(request.settings.items('kittygit'))

def fork_repo(request, repo):
    settings = get_settings(request)

    username, repo_name = repo.split('/', 1)
    if auth.has_permission(request, 'kittygit:read:%s/%s' % (username, repo_name)):
        auth.add_permission(request, 'kittygit:write:%s/%s' % (request.user, repo_name))


        full_repo_dir = os.path.expanduser(
            '/'.join([settings.get('repo_dir', '~/repos'), request.user, repo_name+'.git'])
        )

        if os.path.isdir(full_repo_dir):
            raise NappingCatRejected("That repository has already been forked, silly.")
        os.makedirs(full_repo_dir)

        args = [
            settings.get('git', 'git'),
            '--git-dir=.',
            'clone',
            '--mirror',
            os.path.expanduser(
                '/'.join([settings.get('repo_dir', '~/repos'), username, repo_name+'.git'])
            ),
            './',
        ]

        returncode = subprocess.call(
            args=args,
            cwd=full_repo_dir,
            stdout=sys.stderr,
            close_fds=True,
        )
    else:
        raise NappingCatRejected("You don't have permission to read %s.git. Sorry!" % repo)

def create_repo(request, repo_name, private=False):
    settings = get_settings(request)
    if auth.has_permission(request, 'kittygit:create'):
        auth.add_permission(request, 'kittygit:write:%s/%s' % (request.user, repo_name))
        full_repo_dir = os.path.expanduser(
            '/'.join([settings.get('repo_dir', '~/repos'), request.user, repo_name+'.git'])
        )
        if os.path.isdir(full_repo_dir):
            raise NappingCatRejected("That repository already exists, silly.")
        os.makedirs(full_repo_dir)
        args = [
            settings.get('git', 'git'),
            '--git-dir=.',
            'init',
            '--bare',
        ]
        returncode = subprocess.call(
            args=args,
            cwd=full_repo_dir,
            stdout=sys.stderr,
            close_fds=True,
        )
        pass#okay
    pass

def handle_git(request, action):
    settings = get_settings(request)
    command, subcommand, repo = None, None, None
    if action in (' receive-pack ', ' upload-pack '):
        command, subcommand, repo = request.command.split(' ', 2)
    else:
        command, repo = request.command.split(' ', 1)

    parsed_repo = repo[1:-1][:-4]       # remove quotes and .git extension
    newcommand = None

    okay = (action in (' receive-pack ', '-receive-pack ') and auth.has_permission(request, 'kittygit:write:%s' % parsed_repo)) 
    okay = okay or (action in (' upload-pack ', '-upload-pack ') and auth.has_permission(request, 'kittygit:read:%s' % parsed_repo))
    if okay:
        newcommand = ' '.join([('git%s'%action.strip()), ("'%s/%s.git'" % (os.path.expanduser(settings.get('repo_dir', '~/repos')), parsed_repo))])
        args = [settings.get('git', 'git'), ['git', 'shell', '-c', newcommand]]

        os.execvp(*args)
    else:
        raise NappingCatRejected("""
            You don't have permission to do that.
        """.strip())
