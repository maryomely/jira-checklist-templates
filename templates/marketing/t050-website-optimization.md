# Website optimization checklist
## Technical Optimization
- Configure site mirrors correctly
> Make sure there’s only 1 accessible URL version for each page
> Set up the 301 redirect for non-canonical versions
- Check hreflang tags (for multi-language websites)
- Implement structured data on your website / audit its usage
- Check the availability of your content to crawlers
- Confirm key URLs return HTTP 200
- Check robots.txt does not block important paths
- Submit a valid XML sitemap in Search Console
- Remove multi-hop redirect chains
- Point canonical tags to the right master URL
- Test key templates for JavaScript rendering issues
- Fix orphaned pages and high-value 404s
- Review the SILO structure of your website and make updates, if needed
> Group pages into categories and interlink related pages to tell Google and agents how they are connected
- Optimize Performance Speed and Core Web Vitals
> These metrics are measured on real mobile users at the 75th percentile
> * Check that LCP is under 2.5 seconds
> * Check that INP is under 200 milliseconds
> * Check that CLS is below 0.1
- Remove unused third-party scripts
- Configure Open Graph tags
- Confirm SSL is valid and applied site-wide
- Test on real devices and set regression alerts
- Set up a Technical SEO dashboard for further monitoring
> https://www.coupler.io/dashboard-examples/technical-seo-dashboard
## Content and Technical On-Page SEO
- Check that all publications have unique title tags within the 40–60 character range
- Check that they have unique meta descriptions within 140-160 characters
- Use one H1 and keep H2/H3 levels in order
- Fix broken links and vague anchor text
- Add descriptive alt text to every image
- Check that each page has a specific semantic intent that is not duplicated
- Refresh content older than 3 months (may vary depending on niche)
> You can adjust your content update schedule depending on competitor activity / accepted practices in your niche. Content may age faster or slower depending on your industry and audience.
## AEO
- Allow AI bots in robots.txt
> Such as GPTBot, ClaudeBot, and PerplexityBot
- Add a link to your XML sitemap in robots.txt and keep the sitemap current
- Add Content-Signal preferences to robots.txt
> Example:
> Content-Signal: ai-train=yes, ai-input=yes, search=yes
- Publish an llms.txt file with your key pages and key facts about your product
- Set up automatic Markdown conversion at your CDN, server, or CMS level
> When an AI agent asks for your page, it should get a clean Markdown version instead of heavy HTML. This makes your content easier to process and increases citation accuracy.
- Confirm each article shows a visible last-updated date
- Audit your server logs to understand which pages are crawled by LLMs and how
> * Which content is the most interesting to AI bots
> * Which pages are used for training
> * Where AI bots hallucinate and try to access links that do not exist
### Content AEO
- Open with a direct answer or TL;DR in the first 100 words
- Phrase headings as user questions
- Back key claims with a specific number and a link to the source
- Format processes as lists and comparisons as tables
- Call each product and entity by one consistent name and include definitions
## UX and Conversion Rate Optimization
- Put the primary CTA above the fold
- Cut form fields and set mobile input types
- Keep key pages accessible within three clicks
- Review the conversion flow for friction points
- Use action verbs in every CTA
- Track scroll depth and rage clicks
- A/B test one high-traffic template per quarter
- Keep popups from blocking mobile content
