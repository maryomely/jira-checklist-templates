## API documentation and access
- Collect the API documentation and confirm the schema version under test
- Check the base URL and the environment
- Create accounts with different permission levels
- Request test credentials and save them to the team password manager
- Prepare test data for required and optional fields
## Contract and schema
- Compare each request with the documented schema
- Check response field names and data types
- Send a request without a required field and confirm it is rejected
- Send a request without optional fields and see that it goes through
- Make sure default values match the documentation
## Core requests
- Send a valid request to each endpoint and check the success status code
- Confirm the response body contains the expected records
- Repeat a GET request and see that the created record persists
- Update a record and make sure only the intended fields change
- Delete a record, then check the response code and the record itself
- Try the pagination, sorting, and filtering parameters
## Error handling
- Send invalid data types and check for the 400 response
- Send an empty payload and read the error message
- Request a non-existent resource and confirm the 404 response
- Compare the error format across all endpoints
- Look through error responses for stack traces and internal paths
## Authentication and authorization
-! Send a request without a token and confirm the 401 response
-! Try to read and modify data from another account
- Use an expired token and see that it is rejected
- Go through role-based permissions on every endpoint
## Reliability and limits
- Exceed the rate limit and check the 429 response and its headers
- Send the same request twice and look for a duplicate record
- Measure response time of the most used endpoints against the agreed limit
- Confirm the API version in use is the one under test
## Reporting
- Log every defect with the request, the response, and the status code
- Record tested endpoints and their results in the test report
