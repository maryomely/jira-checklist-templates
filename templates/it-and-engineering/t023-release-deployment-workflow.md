# Pre-QA Steps @developer_user_id
- Verify the Jira release/version is created and linked to relevant tickets
- Ensure release branches (back-end and front-end) are up to date
- Confirm release pull requests (PRs) are created and passing tests
- Add QA notes to tickets where necessary
- Link release Pull Request to the Jira release
- Verify that the release Pull Request has no merge conflicts
# Preparation @qa_owner_user_id
- List feature flags to be updated for regression and production
- Start a Slack/Teams release thread and link it to the Jira release ticket
- Prepare draft release notes/KB article if new features or UI/UX improvements are included
- Schedule the release event in the calendar
> Choose a time within working hours of the engineer with production access. Include one QA and one software engineer and check vacation days.
# Staging Release @developer_user_id
- Merge changes into the staging branch and deploy to the staging environment
- Confirm the build is deployed successfully
- Change status for the tickets deployed to testing environment to “Selected for release”
- Notify QA via the release thread in Slack to start regression testing
# Regression Testing @qa_owner_user_id
- Run regression tests based on defined test cases
- Log any release blockers in Jira and link them to the release ticket
- Move verified tickets to “QA Approved” and approve the release Pull Request
- On success, notify the team and hand back to @developer_user_id for production release
# Production Release @developer_user_id
- Update version numbers and create a PR from staging -> production
- Merge to production and create a Git tag for the release
- Wait for successful deployment notification
- Check that the production app is online
- Verify there are no new errors in monitoring system
- Announce the release in the Slack/Teams thread
- Update environment variables (if needed)
# Marketplace Release @qa_owner_user_id/@developer_user_id
- Publish the new version on the Atlassian Marketplace
- Finalize and publish release notes and the Knowledge Base article
- Conduct quick smoke testing post-release
- Notify the team and support about the release, highlighting fixes and new features
# Post-Release Actions
- Back-merge production -> development_branch to keep branches in sync
- Mark release and related Jira tickets as “Released”
- Monitor key metrics and logs for the first 24–48 hours
- Celebrate 🙂
