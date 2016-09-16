# Contributing

We track stuff that needs doing over in
[issues](https://gitlab.com/tannerlake/dungeonbot/issues).

### Want to help out? Great! Here's how:

- Check out a new branch for your work from `dev` branch.

- Do your thing.
     - Be sure to update any relevant help text.
     - Try to be PEP8 compliant.

- When your changes are ready to be merged back into `dev` branch, do a
  `git pull --rebase` from `dev` to make sure your branch is up to date with
  the most recent `dev` and to replay your changes over the updated `dev` work.

- Resolve any merge conflicts, of course, and push your updated branch.

- Use `git rebase -i HEAD~x` (where `x` is the number of recent commits you
  would like to see) to clean up your commit history; the goal is to squish
  your work into a clean and sensible flow, and to weed out things like five
  consecutive "typo fix" commits.

- Force-push your cleaned-up personal branch (I don't care about rewriting
  history in these small auxiliary branches - I'd rather have a cleaner,
  easier-to-follow history in `master`).

- Make a merge request from your new branch back into `dev`.
     - If your work addresses an issue, please reference it in the body of
       the MR.
     - If your work resolves an issue, please use Git's issue-resolution
       keywords in the body of the MR (examples: `closes #1`, `fixes #1`, etc.)
