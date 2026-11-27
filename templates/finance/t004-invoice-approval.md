- Review the invoice documents
> * Invoice number
> * The entity to which it was issued
> * Type of services – see the [payment structure](payment_structure_url)
> * Check if the descriptions and amounts are correct
- Verify the invoice date and due date
> * Ensure the due date is realistic and fits the payment schedule
> * Flag any invoices with outdated or missing due dates
- Check for duplicate invoice entries in the system
> * Search by invoice number and vendor name
> * If a duplicate is found, tag it as “Duplicate” and notify the Finance team
- Confirm the vendor is approved and active in the database
- Verify the vendor’s banking and contact details
- Fill in the following fields for each ticket:
> * Payment source (see the [payment structure](payment_structure_url))
> * Proper account (see the [Chart of Accounts](chart_of_accounts_url))
> * If you need more details about the payment, contact the Requestor in the ticket comments
- Attach supporting documents
> * Purchase order (if applicable)
> * Contract or agreement (if applicable)
> * Internal approval from the budget owner
- Open the Vendor payments monitor, refresh the data, and reset the dashboard
- Filter PAY-project tickets in the Status Group “To Do” and “In Progress”, Project = project_key
- Review the monitor for payments that go over budget, report to @financial_analyst_user_id, and check if we can pay the specified amount. If not, change the status to “Blocked” and inform the Requestor about this issue in the ticket comments.
- Check the monitor for W-forms. Each vendor must have a signed W-8/W-9 form before we make a payment.
> * If this is the first payment to this vendor, send them a proper W-form using [tax form template](tax_form_template_url)
> * Read more about [W-form guidance](tax_form_guide_url)
- Double-check tax implications for this payment
> * Validate whether VAT, withholding tax, or local tax applies
> * Document the tax treatment in the ticket comments
- Review the total amount to be paid per bank account. If it goes over the current balance, initiate a top-up process using [top-up guide](top_up_guide_url)
- Confirm approvals before scheduling payment
> * Verify required approvals (e.g., team lead, finance manager) are logged in the ticket comments or attached
> * If the approvals are missing, tag @approver_user_id and wait for confirmation
- Mark the invoice as approved and ready for payment - change its status to “Approved”
- Hand the invoice off to the payment execution team
> * Mention @payments_team_mention with a note: “Invoice invoice_number is ready for processing”
> * Include the payment deadline and any special handling notes
