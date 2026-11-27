# Publishing only the latest snapshot

The public repository and `skills/write-jira-checklist.zip` represent the current snapshot. Keep historical source bundles, private test-issue backups, and earlier ZIPs outside this repository. Do not create version tags or historical release assets.

A force push changes the branch history but may leave old commit URLs accessible. To publish a snapshot with no older objects in its repository network, prepare and validate a clean repository containing only one root commit, then replace the public repository. Preserve the existing repository locally first. Verify unauthenticated access to old commit URLs afterward; do not claim that third-party downloads or caches were erased.

After replacing the repository, restore private vulnerability reporting, metadata, and main-branch protections. Run CI before enabling required checks. The owner maintains publication permissions; contributors use pull requests reviewed by the code owner. A solo owner's own pull request cannot supply an independent approval. Owner bypass is reserved for publishing a previously validated snapshot.

Dependabot is configured to propose dependency updates. Review those proposals; do not auto-merge or retain old release assets as part of publication. If old snapshots must remain inaccessible by direct GitHub URLs, use a clean repository replacement for the next publication as well, rather than assuming a squash removes stored objects.
