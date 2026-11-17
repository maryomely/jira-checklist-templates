## Scope and thresholds
- Define the target metrics: response time, throughput, and error rate
-! Agree on the pass thresholds with the team and add them to this checklist
- Name the user flows to cover, for example, login, search, and checkout
- Set the share of traffic each flow gets
> For example, 70% browse and 10% checkout
- Define the expected peak load in concurrent users or requests per second
- Set the ramp-up time and the duration of the peak load
## Environment and data
- Compare the test environment configuration with production and note the differences
- Prepare a data volume that reflects real usage
- Check that the load generator can produce the target load without saturating
- Turn on monitoring for the servers, the database, and the application logs
## Baseline
- Run the script with a few users to confirm it works before the full run
- Measure response time for each flow with a single user
- Record the baseline numbers for later comparison
## Peak load run
- Book the test window with the team so nobody else uses the environment
- Ramp up to the expected peak load over the agreed time
- Hold the peak load for the agreed duration
- Confirm that responses contain the expected content, not only a success status code
- Watch the error rate during the run and stop the test if it exceeds the agreed limit
## Results and reporting
- Read response times as the 90th and 95th percentile, not as averages
- Compare peak response times for each flow with the thresholds and the baseline
- Compare the results with the previous load test run
- Check CPU, memory, and database load during the peak window
- List the flows that missed their threshold
- Record the numbers, the thresholds, and the pass or fail decision
- Create a work item for every flow that missed its threshold
