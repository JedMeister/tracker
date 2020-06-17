Recommended Git Flow
====================

All TurnKey source code is managed by `git`_, and hosted on 
`GitHub`_ in one of the following organizations:

* `turnkeylinux`_: TurnKey related components and projects.
* `turnkeylinux-apps`_: TurnKey appliances.

Not only is `GitHub`_ used to host the source code, but also to
facilitate collaboration via `forks`_ and `pull requests`_. 

There are infinate ways to develop with git, but when teams and
collaborators are involved it's recommended to follow some sort of flow
and guidelines. The most widely acceptable flows are `git-flow`_ and
`GitHub flow`_.

Guidelines
----------

TurnKey related development is loosly based on the GitHub flow, and
follows these guidelines:

* Anything in the master branch is deployable - builds successfully and
  is tested to work.
* When working on something new, whether it be a bugfix or new feature,
  create a descriptively named branch off of master. Each new branch 
  should address just one issue (i.e. create a separate branch from 
  master for each issue).
* Commit to that branch locally and regularly. Source code should be
  documented and rational for changes included in commits.
* When you need feedback or help, or you think the branch is ready for
  merging, open a pull request.
* After someone else has reviewed and signed off on the changes, the
  project maintainer or a core developer will perform the merge in the
  official repository.
* Once it is merged and pushed to master, the project should be rebuilt
  and released ASAP.

Setup
-----

Create a GitHub account
'''''''''''''''''''''''

As hinted above, all our collaboration is done via GitHub. If you don't
already have a GitHub account, you'll need one. So please `sign up for a
free GitHub account`_.

Configure local git on your TKLDev
''''''''''''''''''''''''''''''''''

Configure git so it knows who you are. Change the first 2 lines below to use
your name (or username) and your email address. It's best to use the same
email that your GitHub account uses. Log into your TKLDev and open your
``~/.bashrc.d/git`` file and look for the following lines::

   #export GIT_AUTHOR_NAME="Your Name"
   #export GIT_AUTHOR_EMAIL="your@email.com"
   #export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME
   #export GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

Remove the "hash" (aka "pound") symbol from the start of each of those lines
and update with your name and email. E.g. here's how the first 4 lines of
Jeremy's looks::

   export GIT_AUTHOR_NAME="Jeremy Davis"
   export GIT_AUTHOR_EMAIL="jeremy@turnkeylinux.org"
   export GIT_COMMITTER_NAME=$GIT_AUTHOR_NAME
   export GIT_COMMITTER_EMAIL=$GIT_AUTHOR_EMAIL

To ensure that this new info is used, either log out and log back in, or
source this file, like this::

   . ~/.bashrc.d/git

Configure SSH GitHub authentication for your TKLDev
'''''''''''''''''''''''''''''''''''''''''''''''''''

In order to ``git push`` your changes from your TKLDev to GitHub,
authentication is required. GitHub recommends HTTPS authentication. However,
we believe that for commandline dev systems such as TKLDev, SSH authentication
is a superior option.

If you have already generated an SSH keypair on your TKLDev, then you can just
reuse the existing pair. If you already have an SSH keypair somewhere else, it
is **NOT** recommended that you copy it across and reuse it! Instead, generate
a new keypair.

*Generate a new keypair*

To generate a new SSH keypair, log into your TKLDev via SSH and run the below
command. Be sure to update the email address, ideally use the same one that is
linked to yoru GitHub account::

   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

It will ask where you wish to save it. Unless you have reason to save it
elsewhere, the default should be fine (i.e. just hit enter). It will then ask
for a passphrase (sort of like a password, but as the name suggests, instead of
a word, it's a phrase). If you wish to make it extra secure, you can set one.
But if you are the only person using your TKLDev, you could choose to leave it
blank (and just hit enter again). It will ask for you to repeat your
passphrase, do that and hit enter again (or just enter if you didn't set one).
Note, that if you do not set a passphrase, you should remove the keypair from
your GitHub account if you ever lose access to your TKLDev.

Here's is the example output for Jeremy on a new TKLDev::

   root@tkldev ~# ssh-keygen -t rsa -b 4096 -C "jeremy@turnkeylinux.org"

   Generating public/private rsa key pair.
   Enter file in which to save the key (/root/.ssh/id_rsa):
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /root/.ssh/id_rsa.
   Your public key has been saved in /root/.ssh/id_rsa.pub.
   The key fingerprint is:
   SHA256:tKJIAz9ETkUr8JnZZl+cM5kdNc2687ulpyIuL/pNIh8 jeremy@turnkeylinux.org
   The key's randomart image is:
   +---[RSA 4096]----+
   |. ooo     ..oo   |
   | * = . . = . .o  |
   |. O =   X .  .   |
   | + + . o +  .    |
   |  =   o S    .   |
   | . + . .    o    |
   |  . . . E .  o  .|
   |       oo=. . .o.|
   |      .oo=+. .== |
   +----[SHA256]-----+

*Add the public key to your GitHub Profile*

Once that is complete, (assuming the default filename) output the public key
component like this::

   cat ~/.ssh/id_rsa.pub

That should display a long string (it will display over multiple lines, but is
actually just one long line) which starts with ssh-rsa and ends with your
email. E.g. something like this::

   ssh-rsa AB3Nza[...lots of random characters...]+Cpg3WbD jeremy@turnkeylinux.org

Copy all of that (including the 'ssh-rsa' at the start and your email at the
end). Mac and Linux users who are using the built in SSH client can use the
terminal's "copy" feature. Windows users using PuTTY can copy simply by
selecting the relevant text in the PuTTY session. For other scenarios, please
consult relevant docs.

Then open your `GitHub account's keys page`_ and click the "New SSH key"
button. Select a useful "title" for your key and paste the key string into the
"Key" box. Click "Add SSH key" and you should be good.

For further details, please consult the relevant `GitHub SSH key docs`_.


Make changes walk through
-------------------------

This walkthrough assumes that you are pushing an update or improvement to
existing TurnKey code. If you're hoping to push a new appliance, then hopefully
you know how to create a new repo in your own account.

Fork and clone the source
'''''''''''''''''''''''''

Next, fork the project you want to hack on:

* Log into `GitHub`_, and browse to the projects repository.
* Click the ``fork`` button.

That's it. You've successfully forked the project repository, but so far
it only exists on GitHub.

To be able to work on the project you'll need to clone it. If copying via your
browser, be sure to select the SSH url. The clone command look like this::

    git clone git@github.com:USERNAME/PROJECTNAME.git

So far so good. When a repository is cloned, it has a default ``remote``
called ``origin`` that points to the URL that you cloned. If you cloned your
fork on GitHub then that will be the ``origin``. You will want to keep track
of TurnKey, and perhaps others, so you can add them as remotes too.

It is something of a convention to name the remote repository of the upstream
software (i.e. TurnKey in this case) ``upstream``. Personally, I prefer to
use really explicit remote names though. So I always name TurnKey remotes
``turnkey``.

To add an alternate remote (named ``upstream`` in this case) to a git repo
and pull any updates::

    cd PROJECTNAME
    git remote add upstream https://github.com/ORGANIZATION/PROJECTNAME.git

    # Fetch any new changes to the original repository
    git fetch upstream

    # Merge any changes fetched into your working branch
    git merge upstream/master

You can double check what remotes are configured (all git commands need to be
run within the local git repo). View all remotes like this::

   git remote -v

That will return a list of remotes and the URLs associated. For example, here
is what my Core respository notes when I run ``git remote -v``::

   origin	git@github.com:JedMeister/core.git (fetch)
   origin	git@github.com:JedMeister/core.git (push)
   turnkey	git@github.com:turnkeylinux-apps/core.git (fetch)
   turnkey	git@github.com:turnkeylinux-apps/core.git (push)


Make your changes
'''''''''''''''''

* **Create a branch**: Note that you have only one ``pull request`` per branch::

    git checkout -b DESCRIPTIVE_BRANCH_NAME

* **Hack away**: Make your changes, test and commit as you go. Remember please only address one issue per branch/pull request
* **Test**: Perform final testing.

Push changes and submit a Pull Request
''''''''''''''''''''''''''''''''''''''

Now that you're finished hacking and all changes are committed, you need
to push them to your GitHub repository::

    git push origin DESCRIPTIVE_BRANCH_NAME

Last thing to do is send a ``pull request`` so the maintainer or one of
the core developers can review, sign off, and perform the merge in the
official repository.

* Browse to https://github.com/USERNAME/PROJECTNAME/tree/DESCRIPTIVE_BRANCH_NAME
* Click ``Pull Request``, describe the change and click ``Send pull request``.

Hooray! You did it.

If for some reason the maintainer or one of the core developers has a
problem with your change, they won't want to merge until fixed.

The good news is that whenever you commit and push more changes to that
branch of your code, they will be included in that original pull request
until it is closed.


.. _git: http://git-scm.com/documentation
.. _GitHub: https://github.com
.. _turnkeylinux: https://github.com/turnkeylinux
.. _turnkeylinux-apps: https://github.com/turnkeylinux-apps
.. _forks: https://help.github.com/articles/fork-a-repo
.. _pull requests: https://help.github.com/articles/using-pull-requests
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model
.. _GitHub flow: http://scottchacon.com/2011/08/31/github-flow.html
.. _sign up for a free GitHub account: https://github.com/join
.. _GitHub account's keys page: https://github.com/settings/keys
.. _GitHub SSH key docs: https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
