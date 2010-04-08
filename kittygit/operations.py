import os
import sys
import subprocess
from kittygit.exceptions import KittyGitRepoExists, KittyGitUnauthorized, KittyGitBadParameter
from nappingcat.exceptions import NappingCatException
def fork_repository(git, from_directory, to_directory, output=sys.stderr):
    if not os.path.isdir(from_directory):
        raise NappingCatException("'%s' is not a valid repository." % from_directory)

    if os.path.isdir(to_directory):
        raise KittyGitRepoExists(to_directory)
    os.makedirs(to_directory)
    args = [
        git, '--git-dir=.', 'clone', '--mirror', from_directory, './'
    ]
    return 0 == subprocess.call(
        args=args,
        cwd=to_directory,
        stdout=output,
        close_fds=True,
    )

def create_repository(git, directory, template_dir=None, bare=True):
    if os.path.isdir(directory):
        raise KittyGitRepoExists(directory)
    args = [
        git, '--git-dir=.', 'init',
    ]
    if bare:
        args.append('--bare')
    if template_dir:
        if not os.path.isdir(template_dir):
            raise KittyGitBadParameter("""
                The template directory '%s' is invalid.
            """.strip() % (template_dir))
        args.append('--template=%s'%template_dir)
    os.makedirs(directory)
    return 0 == subprocess.call(
        args=args,
        cwd=directory,
        stdout=sys.stderr,
        close_fds=True,
    )

def git_shell(git, action, directory):
    if not os.path.isdir(directory):
        raise KittyGitBadParameter("%s is not a valid repository." % directory)
    command = 'git%s' % action.strip()
    arg = "'%s'" % directory
    args = [git, 'shell', '-c', ' '.join([command, arg])]
    return 0 == subprocess.call(
        args=args,
        cwd=directory,
        stdout=sys.stdout,
        stderr=sys.stderr,
        stdin=sys.stdin
    )

 
