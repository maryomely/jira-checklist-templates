# Create a user migration plan #must
> Please keep in mind that Jira Cloud Migration Assistant migrates all users and groups as well as users and groups related to selected projects
- Sync your user base
- Verify synchronization
- External users sync verification
- Active external directory verification
## Check your Jira Server version #must
- Verify via user interface or Support Zip Product Version Verification
> Jira Migration Assistant will not work unless Jira is running on a supported version
## Fix any duplicate email addresses #must
- Verify using SQL
> Duplicate email addresses are not supported by Jira Cloud and therefore can’t be migrated with the Jira Cloud Migration Assistant. To avoid errors, you should find and fix any duplicate email addresses before migration. If user information is managed in an LDAP Server, you will need to update emails there and sync with Jira before the migration. If user information is managed locally, you can fix them through the Jira Server or Data Center user interface.
## Make sure you have the necessary permissions #must
- System Admin global permissions on the Server instance
- Exists in the target Cloud site
- Site Administrator Permission in the cloud
## Check for conflicts with group names #must
- Make sure that the groups in your Cloud Site don’t have the same names as groups in Server
> Unless you are actively trying to merge them
- Delete or update add-on users to avoid migration issues
- Verify via SQL
## Update firewall allowance rules #must
- None of the domains should be blocked by firewall or proxy
## Find a way to migrate apps #must
- Contact app vendors
## Check public access settings #must
- Projects
- Filters
- Boards
- Dashboards
## Review server setup #must
- At least 4 GB of heap allocation
- Open Files limit review
- Verify via support zip
## Check server time zone #must for merging Cloud sites
- Switch to UTC if using any other time zone
> Add a system flag to the Jira Server instance -Duser.timezone=UTC as outlined in this article about updating documentation to include timezone details.
## Fix any duplicate shared configuration
## Storage limits
## Prepare the server instance
- Check data status
- All fields have values and are not null
- Any archived projects you wish to migrate are activated
## Prepare your cloud site
- Same Jira products enabled
- Same language
- User migration strategy
## Data backup
- Back up the Jira Server site
- Back up the Cloud site
## Run a test migration
- Done
## Notify Jira support
- Get in touch with Jira migration support
