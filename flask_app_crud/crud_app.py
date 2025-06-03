import os
import sqlite3
import datetime
from flask import Flask, render_template, g, request, redirect, url_for, flash

# Use os.path for cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'db')
PATH = os.path.join(DB_DIR, 'jobs.sqlite')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

def open_connection():
    # Create db directory if it doesn't exist
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    connection = getattr(g, '_connection', None)
    if connection == None:
        try:
            connection = g._connection = sqlite3.connect(PATH)
            connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            app.logger.error(f"Database connection error: {e}")
            raise
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    try:
        connection = open_connection()
        cursor = connection.execute(sql, values)
        if commit == True:
            results = connection.commit()
        else:
            results = cursor.fetchone() if single else cursor.fetchall()

        cursor.close()
        return results
    except sqlite3.Error as e:
        app.logger.error(f"SQL execution error: {e}")
        if commit:
            connection.rollback()
        raise

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

# ===== JOB ROUTES =====

@app.route('/')
@app.route('/jobs')
def jobs():
    try:
        jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
        return render_template('index.html', jobs=jobs)
    except Exception as e:
        app.logger.error(f"Error in jobs route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/job/<job_id>')
def job(job_id):
    try:
        job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
        return render_template('job.html', job=job)
    except Exception as e:
        app.logger.error(f"Error in job route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/job/create', methods=('GET', 'POST'))
def job_create():
    try:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            salary = request.form['salary']
            employer_id = request.form['employer_id']
            
            if not title or not description or not salary or not employer_id:
                flash('All fields are required!')
                employers = execute_sql('SELECT id, name FROM employer')
                return render_template('job_form.html', employers=employers)
            
            execute_sql('INSERT INTO job (title, description, salary, employer_id) VALUES (?, ?, ?, ?)',
                      (title, description, salary, employer_id), commit=True)
            
            flash('Job created successfully!')
            return redirect(url_for('jobs'))
        
        employers = execute_sql('SELECT id, name FROM employer')
        return render_template('job_form.html', employers=employers)
    except Exception as e:
        app.logger.error(f"Error in job_create route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/job/<job_id>/update', methods=('GET', 'POST'))
def job_update(job_id):
    try:
        job = execute_sql('SELECT * FROM job WHERE id = ?', [job_id], single=True)
        
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            salary = request.form['salary']
            employer_id = request.form['employer_id']
            
            if not title or not description or not salary or not employer_id:
                flash('All fields are required!')
                employers = execute_sql('SELECT id, name FROM employer')
                return render_template('job_form.html', job=job, employers=employers)
            
            execute_sql('UPDATE job SET title = ?, description = ?, salary = ?, employer_id = ? WHERE id = ?',
                      (title, description, salary, employer_id, job_id), commit=True)
            
            flash('Job updated successfully!')
            return redirect(url_for('job', job_id=job_id))
        
        employers = execute_sql('SELECT id, name FROM employer')
        return render_template('job_form.html', job=job, employers=employers)
    except Exception as e:
        app.logger.error(f"Error in job_update route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/job/<job_id>/delete', methods=('GET', 'POST'))
def job_delete(job_id):
    try:
        job = execute_sql('SELECT job.id, job.title, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
        
        if request.method == 'POST':
            execute_sql('DELETE FROM job WHERE id = ?', [job_id], commit=True)
            flash('Job deleted successfully!')
            return redirect(url_for('jobs'))
        
        return render_template('confirm_delete.html', 
                              item_type='job', 
                              item_id=job_id, 
                              item_name=f"{job['title']} at {job['employer_name']}")
    except Exception as e:
        app.logger.error(f"Error in job_delete route: {e}")
        return render_template('error.html', error=str(e))

# ===== EMPLOYER ROUTES =====

@app.route('/employer/<employer_id>')
def employer(employer_id):
    try:
        employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
        jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
        reviews = execute_sql('SELECT id, review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
        return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)
    except Exception as e:
        app.logger.error(f"Error in employer route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/employer/create', methods=('GET', 'POST'))
def employer_create():
    try:
        if request.method == 'POST':
            name = request.form['name']
            
            if not name:
                flash('Employer name is required!')
                return render_template('employer_form.html')
            
            execute_sql('INSERT INTO employer (name) VALUES (?)', (name,), commit=True)
            
            flash('Employer created successfully!')
            return redirect(url_for('jobs'))
        
        return render_template('employer_form.html')
    except Exception as e:
        app.logger.error(f"Error in employer_create route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/employer/<employer_id>/update', methods=('GET', 'POST'))
def employer_update(employer_id):
    try:
        employer = execute_sql('SELECT * FROM employer WHERE id = ?', [employer_id], single=True)
        
        if request.method == 'POST':
            name = request.form['name']
            
            if not name:
                flash('Employer name is required!')
                return render_template('employer_form.html', employer=employer)
            
            execute_sql('UPDATE employer SET name = ? WHERE id = ?', (name, employer_id), commit=True)
            
            flash('Employer updated successfully!')
            return redirect(url_for('employer', employer_id=employer_id))
        
        return render_template('employer_form.html', employer=employer)
    except Exception as e:
        app.logger.error(f"Error in employer_update route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/employer/<employer_id>/delete', methods=('GET', 'POST'))
def employer_delete(employer_id):
    try:
        employer = execute_sql('SELECT * FROM employer WHERE id = ?', [employer_id], single=True)
        
        if request.method == 'POST':
            # Delete associated jobs and reviews (cascade delete)
            execute_sql('DELETE FROM review WHERE employer_id = ?', [employer_id], commit=True)
            execute_sql('DELETE FROM job WHERE employer_id = ?', [employer_id], commit=True)
            execute_sql('DELETE FROM employer WHERE id = ?', [employer_id], commit=True)
            
            flash('Employer and all associated jobs and reviews deleted successfully!')
            return redirect(url_for('jobs'))
        
        return render_template('confirm_delete.html', 
                              item_type='employer', 
                              item_id=employer_id, 
                              item_name=employer['name'],
                              warning='This will also delete all associated jobs and reviews!')
    except Exception as e:
        app.logger.error(f"Error in employer_delete route: {e}")
        return render_template('error.html', error=str(e))

# ===== REVIEW ROUTES =====

@app.route('/employer/<employer_id>/review', methods=('GET', 'POST'))
def review(employer_id):
    try:
        if request.method == 'POST':
            review = request.form['review']
            rating = request.form['rating']
            title = request.form['title']
            status = request.form['status']

            date = datetime.datetime.now().strftime("%m/%d/%Y")
            execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)', 
                      (review, rating, title, date, status, employer_id), commit=True)

            flash('Review added successfully!')
            return redirect(url_for('employer', employer_id=employer_id))

        return render_template('review.html', employer_id=employer_id)
    except Exception as e:
        app.logger.error(f"Error in review route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/review/<review_id>/update', methods=('GET', 'POST'))
def review_update(review_id):
    try:
        review = execute_sql('SELECT * FROM review WHERE id = ?', [review_id], single=True)
        
        if request.method == 'POST':
            review_text = request.form['review']
            rating = request.form['rating']
            title = request.form['title']
            status = request.form['status']
            
            if not review_text or not rating or not title or not status:
                flash('All fields are required!')
                return render_template('review_form.html', review=review)
            
            execute_sql('UPDATE review SET review = ?, rating = ?, title = ?, status = ? WHERE id = ?',
                      (review_text, rating, title, status, review_id), commit=True)
            
            employer_id = review['employer_id']
            flash('Review updated successfully!')
            return redirect(url_for('employer', employer_id=employer_id))
        
        return render_template('review_form.html', review=review)
    except Exception as e:
        app.logger.error(f"Error in review_update route: {e}")
        return render_template('error.html', error=str(e))

@app.route('/review/<review_id>/delete', methods=('GET', 'POST'))
def review_delete(review_id):
    try:
        review = execute_sql('SELECT review.*, employer.id as employer_id FROM review JOIN employer ON employer.id = review.employer_id WHERE review.id = ?', [review_id], single=True)
        
        if request.method == 'POST':
            employer_id = review['employer_id']
            execute_sql('DELETE FROM review WHERE id = ?', [review_id], commit=True)
            
            flash('Review deleted successfully!')
            return redirect(url_for('employer', employer_id=employer_id))
        
        return render_template('confirm_delete.html', 
                              item_type='review', 
                              item_id=review_id, 
                              item_name=review['title'])
    except Exception as e:
        app.logger.error(f"Error in review_delete route: {e}")
        return render_template('error.html', error=str(e))

# Add a basic error template if it doesn't exist
@app.route('/create_error_template')
def create_error_template():
    if not os.path.exists(os.path.join(app.template_folder, 'error.html')):
        with open(os.path.join(app.template_folder, 'error.html'), 'w') as f:
            f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>An error occurred</h1>
    <p>{{ error }}</p>
    <a href="/">Return to home page</a>
</body>
</html>
''')
    return "Error template created"

# Add sample data to the database
@app.route('/add_sample_data')
def add_sample_data():
    try:
        # Add sample employers
        employers = [
            ("Tech Innovations Inc.",),
            ("Global Finance Group",),
            ("Healthcare Solutions",),
            ("Education First",),
            ("Retail Giants",)
        ]
        
        for employer in employers:
            try:
                execute_sql('INSERT INTO employer (name) VALUES (?)', employer, commit=True)
            except:
                pass  # Skip if already exists
        
        # Add sample jobs
        jobs = [
            ("Frontend Developer", "Build user interfaces using React and modern CSS frameworks.", 95000, 1),
            ("Backend Engineer", "Develop robust APIs and database solutions using Python and SQL.", 105000, 1),
            ("DevOps Specialist", "Manage cloud infrastructure and CI/CD pipelines.", 110000, 1),
            ("Financial Analyst", "Analyze market trends and prepare financial reports.", 90000, 2),
            ("Investment Advisor", "Provide investment guidance to high-net-worth clients.", 120000, 2),
            ("Nurse Practitioner", "Provide primary and specialty healthcare.", 115000, 3),
            ("Medical Researcher", "Conduct clinical trials and analyze healthcare data.", 95000, 3),
            ("University Professor", "Teach computer science courses and conduct research.", 85000, 4),
            ("Curriculum Developer", "Design educational content for K-12 programs.", 75000, 4),
            ("Store Manager", "Oversee daily operations of retail location.", 70000, 5),
            ("E-commerce Specialist", "Manage online sales channels and digital marketing.", 80000, 5)
        ]
        
        for job in jobs:
            try:
                execute_sql('INSERT INTO job (title, description, salary, employer_id) VALUES (?, ?, ?, ?)', job, commit=True)
            except:
                pass  # Skip if already exists
        
        # Add sample reviews
        reviews = [
            ("Great place to work with cutting-edge technology.", 5, "Innovative Environment", datetime.datetime.now().strftime("%m/%d/%Y"), "current", 1),
            ("Good benefits but long hours.", 3, "Work-Life Balance Issues", datetime.datetime.now().strftime("%m/%d/%Y"), "former", 1),
            ("Excellent compensation and growth opportunities.", 4, "Great for Career Growth", datetime.datetime.now().strftime("%m/%d/%Y"), "current", 2),
            ("Supportive management and good healthcare benefits.", 5, "Caring Workplace", datetime.datetime.now().strftime("%m/%d/%Y"), "current", 3),
            ("Challenging but rewarding work environment.", 4, "Intellectually Stimulating", datetime.datetime.now().strftime("%m/%d/%Y"), "current", 4),
            ("High pressure sales environment.", 2, "Stressful Targets", datetime.datetime.now().strftime("%m/%d/%Y"), "former", 5)
        ]
        
        for review in reviews:
            try:
                execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)', review, commit=True)
            except:
                pass  # Skip if already exists
        
        return "Sample data added successfully!"
    except Exception as e:
        app.logger.error(f"Error adding sample data: {e}")
        return f"Error adding sample data: {e}"

# Proper entry point for the application
if __name__ == '__main__':
    # Create error template on startup
    with app.test_request_context():
        app.preprocess_request()
        create_error_template()
        add_sample_data()  # Add sample data on startup
    
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0')
