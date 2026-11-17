# Code formatting check
- Are alignments, proper white space, and easily identifiable code block starting and ending points present?
- Has the developer followed correct naming conventions?
- Can the code fit on a standard laptop screen? You shouldn’t need to scroll diagonally on a 14’’ screen.
## Architecture check
- Is it split between presentation, business, and data layers?
- Is it split into files based on technology?
- Is it working with existing technologies and patterns?
## Coding best practices check
- Is the code using constants?
- Are similar values grouped under an enumeration?
- Are the comments informative and beneficial? Do they explain what is being done?
- Is there an excess of if/else blocks?
- Is the code relying on framework features wherever possible rather than relying on custom solutions?
## Maintainability check
- Is the code easily readable by a human being?
- Is the code easily tested?
- Can it be refactored into a separate function?
- Are there flow of control, parameter, and data exception details necessary for debugging?
- Are configurable files kept in place? There must not be a need to make changes if the data changes frequently.
## Reusability check
- Are the same principles not repeated more than once?
- Are reusable services and functions used when applicable?
## Security check
- Validation against SQL injections
- Validation against XSS
- Is sensitive data encrypted?
## Scalability check
- Is the code scalable?
## Usability check
- Is the solution usable from the user’s POV?
## Performance check
- Is the correct data type used?
- Lazy loading, asynchronous and parallel processing
- Caching and session/application data
