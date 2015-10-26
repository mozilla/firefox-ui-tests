## How to contribute
So you want to write code and get it landed in the official Firefox UI Tests repository? Then first fork [our repository](https://github.com/mozilla/firefox-ui-tests) into your own Github account, and create a local clone of it as described in the [installation instructions](https://github.com/mozilla/firefox-ui-tests#installation). The latter will be used to get new features implemented or bugs fixed. Once done and you have the code locally on the disk, you can get started. It's best not to work directly on the mozilla-central branch, but to create a separate branch for each issue you are working on. That way you can easily switch between different work, and you can update each branch individually with the latest changes on upstream mozilla-central . Check also our [best practices for Git](http://ateam-bootcamp.readthedocs.org/en/latest/reference/git_github.html).

### Writing Code
Please follow our [Python style guide](http://ateam-bootcamp.readthedocs.org/en/latest/reference/python-style.html), and also test with [pylama](https://pypi.python.org/pypi/pylama). If something is unclear, look at existing code which might help you to understand it better.

### Submitting Patches
When you think the code is ready for review, a pull request should be created on Github. Your initial commit should have the form `Bug %ID% - %Summary%. r=%reviewer%`; the bug ID is from bugzilla.mozilla.org. For each update to the PR, we automatically run all the tests via [Travis CI](http://travis-ci.org/). If tests are failing, it's best to address the failures before requesting review; otherwise you may wait for a review.

To request review, add a text attachment to the issue at bugzilla.mozilla.org: paste the PR's Github URL into the File box, use "github pull request" as the Description, and then below, flag the attachment for review (or feedback) by choosing "?" from the adjacent menu and adding a proposed reviewer under Requestee.

If your reviewer requests updates, add them to the same branch in a new commit and push to your remote development branch. Remember to request a new review or more feedback at bugzilla, by clicking on the attachment's Details link and updating the flags. Keep in mind that reviews can span multiple cycles until the owners are happy with the new code.

## Managing the Repository

### Merging Pull Requests
Once a PR is in its final state it needs to be merged into the upstream mozilla-central branch. For that please **DO NOT** use the Github merge button! But merge it yourself on the command line. Reason is that we want to have a clean history. Before pushing the changes to upstream mozilla-central, make sure that all individual commits have been squashed into a single one with a commit message in the form `Bug %ID% - %Summary%. r=%reviewer%`. Also check with `git log` to not push merge commits. Only merge PRs where Travis does not report any failure!
