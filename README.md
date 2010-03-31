kittygit
========

a gitosis-alike that uses the [nappingcat](http://github.com/chrisdickinson/nappingcat) framework to
provide single-user git hosting. _in extreme beta mode right now_.

installation
------------ 
install nappingcat as a new user (preferably "git", but "kitten" may also work), and in your `~/nappingcat.conf` file add the following:

    [kittyconfig]
    router = kittygit.patterns
    paths = 
            path/to/nappingcat
            path/to/kittygit

    [kittygit]
    git = <wherever git lives on PATH>
    repo_dir = ~/kittygit

or include it in your existing nappingcat app patterns.

creating a repo
---------------
create a new, empty repo

    ssh git@someplace.com kitty-git create-repo 'repo-name'

will initialize a new bare repository on the server that you can push things to.

forking an existing repo
------------------------
if you have the read permissions to another repository:

    ssh git@someplace.com kitty-git fork 'chris/nappingcat.git'

will create a bare clone of that repository for you that you can clone
 as follows (assuming your name is `gary`):

    git clone git@someplace.com:gary/nappingcat.git

otherwise you can push and pull to the server as you always would.

