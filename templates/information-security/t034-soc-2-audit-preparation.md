## SOC 2 audit preparation governance
- Confirm Information Security Policy, Acceptable Use, and Code of Conduct are reviewed and re-approved
- Attach meeting minutes (board / security steering committee) that cover risk, financial reporting impact, and SOC 2 scope
- Validate that key roles (CISO, CTO, internal auditors) are documented in org chart and Confluence
- Confirm prior-year audit findings and management responses are tracked and linked to Jira issues

## SOC 2 audit preparation communication
- Verify completion of annual security training for all employees in scope (export LMS report and attach as evidence)
- Confirm onboarding and offboarding workflows include security and access steps, with automation in Jira Service Management where possible
- Link to your incident communication runbook in Confluence
- Check that communication channels with external auditors (e.g., engagement letter, PBC list) are documented and filed

## SOC 2 audit preparation risk assessment
- Update risk register and ensure each risk has: owner, likelihood, impact, and mitigation
- Confirm at least one formal risk review held during the fiscal year (attach meeting notes)
- Link high-risk items to Jira initiatives (e.g., infrastructure changes, Data Center to Cloud migration projects)
- Review whether new products or major changes introduced new risks that affect SOC 2 scope

## SOC 2 audit preparation monitoring
- Document quarterly access reviews (admin accounts, production access, financial systems) with evidence attached
- Confirm periodic review of Jira audit log, CI/CD audit logs, and other system logs for anomalies
- Verify that internal audit or compliance reviews were performed (and link related Jira issues)
- Track follow-up on any deviations and corrective actions

## SOC 2 audit preparation control activities
- Confirm change approval workflows in Jira or your DevOps tools are consistently used and documented
- Check segregation of duties between developers, reviewers, and deployers (link Bitbucket/GitHub/GitLab configuration screenshots)
- Validate that critical production changes require peer review and automated tests
- Ensure exception handling and deviations (e.g., emergency changes) are logged and approved

## SOC 2 audit preparation logical access
- Inventory all in-scope systems (AWS, Azure, GCP, Jira Cloud, Confluence, Slack, internal apps)
- Confirm SSO / authentication and MFA are enforced on all production and key business systems
- Validate onboarding and offboarding processes remove access within defined SLAs (e.g., 24 hours)
- Review admin and privileged account access at least quarterly and document the review in Jira

## SOC 2 audit preparation change management
- Confirm all production changes go through a standard pipeline (e.g., from Jira to Bitbucket/GitHub then to CI/CD and to deployment)
- Link example pull requests, build logs, and deployment logs for sampled changes
- Ensure rollback and back-out procedures are documented and tested
- Attach sample evidence for configuration changes (e.g., firewall rules, IAM policies)

## SOC 2 audit preparation operations and incidents
- Confirm monitoring and alerting are configured for key services (availability, performance, security)
- Attach sample alerts and response tickets from Jira Service Management or your incident tool
- Document incident response process, including severity levels, communication, and post-incident actions
- Verify backup jobs, DR tests, and restoration procedures are executed and documented during the period

## SOC 2 audit preparation vendors
- Maintain an up-to-date vendor inventory with owners, data classification, and purpose
- Collect and review SOC 2 reports or security documentation from critical vendors
- Document risk assessment and mitigation for each high-risk vendor
- Confirm contracts and DPAs reflect your regulatory compliance and security requirements
