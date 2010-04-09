kittygit
========

a gitosis-alike that uses the [nappingcat](http://github.com/chrisdickinson/nappingcat) framework to
provide single-user git hosting. _in extreme beta mode right now_.

installation
------------ 
kittygit by itself isn't too useful -- it's best to create a new nappingcat setup that includes it in
it's patterns.

to install, clone the [nappingcat repository](http://github.com/chrisdickinson/nappingcat). it should
follow the this pattern:

*Step 1*

    $ git clone git://github.com/chrisdickinson/nappingcat.git
    $ cd nappingcat
    $ sudo python setup.py install

*Step 2*

    $ sudo adduser \
      --system \
      --shell /bin/bash \
      --gecos 'git version control' \
      --group \
      --disabled-password \
      --home /home/git \
      git
    $ sudo su git
    $ git clone git://github.com/chrisdickinson/kittygit.git
    $ cat > ~/nappingcat.conf
      [kittyconfig]
      router = kittygit.patterns
      paths =
            /home/<first-user>/nappingcat
            /home/git/kittygit
      auth = path.to.auth.backend
      [kittygit]
      git = `which git`
      user = git
      host = <the publicly available url for this server>
      repo_dir = ~/repos
      <press control-D twice>

*Step 3*
This is where having your own nappingcat app comes in useful, since kittygit does not provide an
auth backend (and especially not one that automatically adds SSH Keys, like gitosis).

open ~git/.ssh/authorized_keys (creating the file and directory if it doesn't exist) and add your
key as normal.

Before the `ssh-rsa` part of the key, put 

    command="nappingcat-serve your-user-name",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty 

where `your-user-name` is, suprisingly, your desired user name.

running tests
-------------
clone the kittygiy repo, cd into it, clone the nappingcat repo, and run nosetests.

creating a repo
---------------
create a new, empty repo

    ssh git@someplace.com kitty-git create-repo 'repo-name'

will initialize a new bare repository on the server that you can push things to.

    ssh git@someplace.com kitty-git create-repo 'repo-name' --template='/path/to/template/dir/on/server'

will create a bare repository on the server using the git template directory you've provided. This is useful
for creating repos that have hook scripts.

forking an existing repo
------------------------
if you have the read permissions to another repository:

    ssh git@someplace.com kitty-git fork 'chris/nappingcat.git'

will create a bare clone of that repository for you that you can clone
 as follows (assuming your name is `gary`):

    git clone git@someplace.com:gary/nappingcat.git

otherwise you can push and pull to the server as you always would. This performs the equivalent of a
`git clone --mirror`.
