## Prepare for testing
- Read the acceptance criteria for this feature
- Note the build version and the environment you test on
- Run one core scenario of the feature to confirm the build is testable
- Prepare the accounts and test data this feature needs
- Check which browsers and OS versions this feature must support
## Run the tests
- Run the test cases for this feature, starting with the critical flows
- Record the actual result next to the expected one for every case
- Mark blocked cases and write down what blocks them
- Go through the negative scenarios and the empty states
- Run a regression check on the flows that share components with this feature
## Handle defects
- Log each defect as a separate work item in the QA space, not in the comments
> Title pattern: feature_area what happens and when it happens
> Add steps to reproduce, environment, expected and actual result, and a screenshot or a recording
- Link every defect to this work item
- Set severity and priority for each defect
- Retest every fixed defect, then close it or reopen it with a comment
## Report and hand over
-! Confirm every planned test case is executed, skipped, or blocked for a stated reason
- Summarize what passed, what failed, and what stays open in a comment on this work item
- List the skipped cases and the reason for each one in the same comment
- Update the testing status in the work item
- Notify the team that testing is finished and hand the work item over
