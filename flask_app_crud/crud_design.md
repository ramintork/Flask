# CRUD Functionality Design

## New Routes to Implement

### Jobs
1. **Create Job**
   - Route: `/job/create`
   - Methods: GET, POST
   - Form fields: title, description, salary, employer_id

2. **Update Job**
   - Route: `/job/<job_id>/update`
   - Methods: GET, POST
   - Form fields: title, description, salary, employer_id

3. **Delete Job**
   - Route: `/job/<job_id>/delete`
   - Methods: POST
   - Confirmation required

### Employers
1. **Create Employer**
   - Route: `/employer/create`
   - Methods: GET, POST
   - Form fields: name

2. **Update Employer**
   - Route: `/employer/<employer_id>/update`
   - Methods: GET, POST
   - Form fields: name

3. **Delete Employer**
   - Route: `/employer/<employer_id>/delete`
   - Methods: POST
   - Confirmation required
   - Note: Should cascade delete related jobs and reviews

### Reviews
1. **Update Review**
   - Route: `/review/<review_id>/update`
   - Methods: GET, POST
   - Form fields: review, rating, title, status

2. **Delete Review**
   - Route: `/review/<review_id>/delete`
   - Methods: POST
   - Confirmation required

## Template Updates

### New Templates
1. `job_form.html` - Form for creating/updating jobs
2. `employer_form.html` - Form for creating/updating employers
3. `confirm_delete.html` - Generic confirmation page for deletions

### Existing Template Updates
1. `index.html` - Add "Create Job" and "Create Employer" buttons
2. `job.html` - Add "Edit" and "Delete" buttons
3. `employer.html` - Add "Edit" and "Delete" buttons for employer and reviews

## Database Schema Updates
- No schema changes needed, current tables support CRUD operations
- Tables: job, employer, review

## UI/UX Considerations
- Consistent styling across all forms
- Clear confirmation messages for all operations
- Error handling with user-friendly messages
- Redirect to appropriate pages after operations
