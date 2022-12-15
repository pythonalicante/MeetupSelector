# How we work with Git

We use __Forking Workflow__[^doc-4] to collaborate in this project.

## Steps to open a Pull Request

1. Fork the [repository](https://github.com/pythonalicante/MeetupSelector/)[^doc-1].
2. Create a `branch` in your local copy with the name `<type>/<ticket>-<description>`[^ex-1].
3. Edit the files and make the commit/s.
4. Push your changes to your `branch`.
5. Open the Pull Request.[^doc-5]

!!! caution
	Each Pull Request must be on top of `main` branch to merge it. In order to achieve this, you have to sync your fork[^doc-2] and rebase[^doc-3] the `main` branch.


## How to write a commit

All the commits should follow the format of __Conventional Commits__[^commit-1], as show in the next example:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### How to write a good commit message

!!! note "Disclaimer"

	This section is a summary of [cbeams](https://cbea.ms/author/cbeams/) article: [How to write a Git Commit message](https://cbea.ms/git-commit/)

!!! note "TL;DR"

	The commit subject must complete the next sentence:

	__If applied, this commit will <u>your subject line here</u>__

	Example:

	* If applied, this commit will update getting started documentation
	* If applied, this commit will remove deprecated methods
	* If applied, this commit will release version 1.0.0
	* If applied, this commit will merge pull request #123 from user/branch

To write a good commit message, it should follow the next directives:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

> To go deeper is each point, please see the article[^commit-2]


[^doc-1]: [How to fork a repo in Github](https://docs.github.com/en/get-started/quickstart/fork-a-repo?tool=webui)
[^doc-2]: [How to sync a fork in Github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork#syncing-a-fork-branch-from-the-web-ui)
[^doc-5]: [Open a Pull Request in Github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
[^doc-3]: [How to rebase a branch](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)
[^doc-4]: [Forking Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
[^commit-1]: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
[^commit-2]: [How to write a Git Commit message](https://cbea.ms/git-commit/)
[^ex-1]: Example: `feat/010-create_topic_endpoint`
