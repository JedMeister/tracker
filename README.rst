===================
TurnKey Dev Tracker
===================

.. contents:: Contents:

Overview
--------

TurnKey uses GitHub's project management features to track development.

Resources:

1) `Issue Tracker`_: used to report and track bugs, issues and
   feature requests related to TurnKey Linux. 

2) `Wiki`_: used to propose and track appliance candidates,
   and also as a general purpose whiteboard for TurnKey development.
   
This tracker is **NOT** intended to be used as:

* A `support forum`_ we already have one of those.
* A `general discussion forum`_, we have one of those as well.

Reporting a bug, issue or feature request
-----------------------------------------

Before creating a new issue on the `Issue Tracker`_, please check to see 
if a similar issue already exists. Please read `How to read the Issue 
Tracker`_ section below for details. Understanding our `Issue
Tracker Workflow`_ might also be useful.

If an issue exists already please post a comment showing it also affects 
you. Knowing an issue effects multiple users is useful when we decide 
how to prioritize limited development resources. Please try and include 
any additional information you think might help.

The ideal bug/issue includes:

1) A detailed description of the issue.
2) How to reproduce the issue step by step.
3) Any extra information that might be relevant, such as appliance
   name, version, deployment (ISO, OpenStack, Amazon EC2), any
   changes made prior to issue, etc.

The ideal feature request includes:

1) A detailed description of feature and component it relates to.
2) One or more use cases for the feature.
3) Any extra information that might be relevant.

Issue Tracker Workflow
----------------------

1) Issue reported on the `Issue Tracker`_ (by you!?)
2) Issue triaged by TurnKey team member:

   - Labelled_ with the appropriate tags. Each issue can have multiple
     tags, e.g.:
     
     - *bug* [red] or *feature* (request) [green];
     - *security* / *critical* (when relevant) [deep red];
     - appliance or software the issue relates to [orange] e.g. *lamp*;
     - appliance build type the issue relates to (when relevant) [
       blue/green] e.g. *ova (buildtype)*;
     - other tags as relevant e.g. *workaround* if a workaround is
       documented, *upstream* if the bug is inherited from elsewhere, 
       etc.

   - Pinned to a milestone_. Each issue can only be pinned to a single
     milestone. I.e.:

     - for appliances, generally the next release e.g. *14.2*;
     - for other software, the next release that we plan e.g. *tklbam
       v1.5*;
     - sometimes one of the more vague milestones: *on ice* or *soon
       (hopefully)*;
     - occasionally none (if we haven't yet decided).

3) A bugfix or feature is developed (by you!? or us) and a PR (pull 
   request) is issued against the relevant repo here on GitHub.
4) Preliminary code review occurs. As need be, considerations are 
   discussed within the PR. 
5) The fix or feature is merged into master branch of relevant repo.
6) Issue is closed.
7) If the bug is considered *critical* or *security* then the appliance
   is re-released (and the bug is re-pinned to the pervious milestone).
8) Rinse and repeat until ready for next version release...
9) Once the new version is released, the milestone is closed and a new 
   (next version) milestone is created. Generally a new version is not 
   released until all the milestone bugs are closed. Any unaddressed
   feature requests and new bugs will be pinned to the new milestone.

How to read the Issue Tracker
-----------------------------

If you have encountered an issue; either a bug or something that could
be much better (i.e. a feature request), have a look on the
`Issue Tracker`_.

By default, the Issue Tracker will display all open issues. The 
"Filter" search box by default will include ``is:issue is:open``. 
Remove ``is:open`` and include the name of the appliance &/or any 
other terms you think might be relevant. Hit enter and all the 
relevant issues (both open and closed) should be displayed. You may 
wish to revise your search to be more or less specific depending on 
the amount of results. 

Between the title and the tags (especially the orange ones) you 
should be able to see whether your issue has been reported already. 
Please note that issues relevant to all appliances will usually 
only be tagged *core*; issues relating to a subset of appliances 
will often only be tagged with the base appliance name. E.g. an 
Apache config bug that effects all LAMP based appliances may only 
be tagged *lamp*.

If the issue you're experiencing has already been reported, you can
further refine your understanding by considering the milestone it's
pinned to and it's state (*open* or *closed*).

**Milestone**:

- Current version (e.g. currently *14.1*)

  - if pinned to the current version milestone then the issue should 
    already be addressed in the current release. If not then
    there are 2 possibilities:

    1) We have re-released the appliance (to include the fix). This
       should be resolved if you retry with the current appliance.
    2) We've made a mistake somewhere along the line. If you think that
       this has happened, please let us know.

- Future version (e.g. current open milestone is *14.2*)

  - if pinned to the next version milestone then the issue hasn't 
    yet been resolved for the current release. To understand the current
    status of an issue pinned to a future release milestone, you will 
    need to also consider it's state (see below).

**State** (*open* or *closed*):

- Open:

  - the issue has not yet been addressed. The issue thread may include 
    additional info about a workaround or other ways to mitigate the 
    issue.

- Closed:

  - the issue has been resolved and code has been merged. However the
    current release may not yet include the fix/update. You will need to
    consider the milestone to be sure.
  
When will a bugfixed appliance be released?
-------------------------------------------

Our `Issue Tracker Workflow`_ means that issues are usually closed 
long before we release a new version. So it is expected that the 
current appliance may still include some of the known bugs. 

Ideally we'd like to re-release an appliance as soon as we have resolved
a bug. However due to limited resources and the re-release overhead, we
prioritize rebuilds on the basis of bug severity. If a bug is critical 
or has serious security implications we will re-release ASAP. If the 
basic functionality of the appliance is not directly effected then we 
will wait for the next release. 

Obviously this decision making process is subjective. If you think that 
we've made a mistake, please comment on the issue and explain your 
perspective and we may reconsider.

If you wish, you can `rebuild the appliance yourself`_, using TKLDev_
and the latest buildcode. `Buildtasks`_ supports building appliances to 
any of our target `build types`_.

Contributing as a developer
---------------------------

TurnKey is 100% open source and the code for all components is right here on GitHub.
Developers with good ideas are strongly encouraged to be bold and contribute code. 
Use the source Luke! 

See the `guidelines and walk through`_.

.. _Issue Tracker: https://github.com/turnkeylinux/tracker/issues/
.. _Wiki: https://github.com/turnkeylinux/tracker/wiki/
.. _support forum: http://www.turnkeylinux.org/forum/support/
.. _general discussion forum: http://www.turnkeylinux.org/forum/general/
.. _Labelled: https://github.com/turnkeylinux/tracker/labels
.. _milestone: https://github.com/turnkeylinux/tracker/milestones
.. _rebuild the appliance yourself: https://www.turnkeylinux.org/docs/howto-build-isos-with-tkldev
.. _TKLDev: https://www.turnkeylinux.org/tkldev
.. _Buildtasks: https://github.com/turnkeylinux/buildtasks
.. _build types: https://www.turnkeylinux.org/docs/builds
.. _guidelines and walk through: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst

