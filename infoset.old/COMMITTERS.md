Terminology
====

Many of these terms have more than one meaning.  For the purposes of this
document, the following terms refer to specific things.

**contributor** - A person who makes a change to Puppet and submits a change
set in the form of a pull request.

**change set** - A set of discrete patches which combined together form a
contribution.  A change set takes the form of Git commits and is submitted to
Puppet in the form of a pull request.

**committer** - A person responsible for reviewing a pull request and then
making the decision what base branch to merge the change set into.

**base branch** - A branch in Git that contains an active history of changes
and will eventually be released using semantic version guidelines.  The branch
named `master` will always exist as a base branch.  The other base branches are
`stable`, and `security` described below.

**master branch** - The branch where new functionality that are not bug fixes
is merged.

**stable branch** - The branch where bug fixes against the latest release or
release candidate are merged.
