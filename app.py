from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample data for projects
PROJECTS_DATA = [
    {
        "id": 1,
        "title": "AI-Powered Study Assistant",
        "description": "An intelligent assistant that helps students organize their study materials and schedule.",
        "technology": ["Python", "AI", "Web"],
        "price": 49.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 95,
        "date_added": "2023-10-15",
        "seller": "TechStudent123",
        "image": "https://via.placeholder.com/300x200?text=AI+Assistant",
        "sales_count": 25
    },
    {
        "id": 2,
        "title": "Smart Campus Navigation",
        "description": "An app that helps students navigate campus with real-time updates.",
        "technology": ["Android", "IoT", "Maps"],
        "price": 29.99,
        "difficulty": "Intermediate",
        "rating": 4,
        "popularity": 87,
        "date_added": "2023-11-02",
        "seller": "CampusDev",
        "image": "https://via.placeholder.com/300x200?text=Campus+Nav",
        "sales_count": 18
    },
    {
        "id": 3,
        "title": "Eco-Friendly Shopping Platform",
        "description": "A web platform connecting consumers with sustainable products.",
        "technology": ["Web", "Python", "Data Science"],
        "price": 39.99,
        "difficulty": "Intermediate",
        "rating": 4,
        "popularity": 78,
        "date_added": "2023-11-10",
        "seller": "GreenTech",
        "image": "https://via.placeholder.com/300x200?text=Eco+Platform",
        "sales_count": 32
    },
    {
        "id": 4,
        "title": "Virtual Lab Simulator",
        "description": "A physics lab simulator for remote learning environments.",
        "technology": ["Web", "JavaScript", "Simulation"],
        "price": 59.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 92,
        "date_added": "2023-10-28",
        "seller": "SciencePro",
        "image": "https://via.placeholder.com/300x200?text=Lab+Simulator",
        "sales_count": 15
    },
    {
        "id": 5,
        "title": "Mental Health Tracker",
        "description": "An app to track mood and provide mental wellness resources.",
        "technology": ["Android", "AI", "Health"],
        "price": 24.99,
        "difficulty": "Beginner",
        "rating": 4,
        "popularity": 83,
        "date_added": "2023-11-05",
        "seller": "WellnessDev",
        "image": "https://via.placeholder.com/300x200?text=Health+Tracker",
        "sales_count": 22
    },
    {
        "id": 6,
        "title": "Blockchain Voting System",
        "description": "A secure voting system using blockchain technology.",
        "technology": ["Blockchain", "Web", "Security"],
        "price": 79.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 88,
        "date_added": "2023-10-20",
        "seller": "SecureVote",
        "image": "https://via.placeholder.com/300x200?text=Voting+System",
        "sales_count": 12
    }
]

# Sample data for top sellers
TOP_SELLERS = [
    {"name": "TechStudent123", "projects_sold": 15, "rating": 4.9},
    {"name": "CampusDev", "projects_sold": 12, "rating": 4.8},
    {"name": "GreenTech", "projects_sold": 10, "rating": 4.7},
    {"name": "SciencePro", "projects_sold": 8, "rating": 4.9},
    {"name": "WellnessDev", "projects_sold": 7, "rating": 4.6}
]

CATEGORY_MAPPINGS = {
    "web_development": ["Web"],
    "app_development": ["Android"],
    "web_application": ["Web"],
    "data_science": ["Data Science"],
    "aiml": ["AI"],
    "blockchain": ["Blockchain"],
    "cyber_security": ["Security"],
    "cloud_computing": ["Cloud"]
}

@app.route('/')
def index():
    # Sort projects for different sections
    trending_projects = sorted(PROJECTS_DATA, key=lambda x: (-x['popularity'], -x['difficulty'].count('High')))
    new_projects = sorted(PROJECTS_DATA, key=lambda x: x['date_added'], reverse=True)
    mini_projects = sorted(PROJECTS_DATA, key=lambda x: x['price'])[:4]  # Mini projects by lowest price
    top_selling_projects = sorted(PROJECTS_DATA, key=lambda x: x['sales_count'], reverse=True)[:3]

    # Get categories
    categories = [
        "Web Development",
        "Mobile App",
        "Web Application",
        "Data Science",
        "Artificial Intelligence",
        "Blockchain",
        "Cybersecurity",
        "Cloud Computing"
    ]

    return render_template('index.html',
                           trending_projects=trending_projects[:4],
                           new_projects=new_projects[:4],
                           mini_projects=mini_projects,
                           top_selling_projects=top_selling_projects,
                           categories=categories,
                           top_sellers=TOP_SELLERS)

@app.route('/sell_your_project', methods=['GET', 'POST'])
def sell_your_project():
    if request.method == 'POST':
        # Process form data
        student_name = request.form.get('student_name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        college_name = request.form.get('college_name')
        course = request.form.get('course')
        year = request.form.get('year')
        project_title = request.form.get('project_title')
        developer = request.form.get('developer')
        project_type = request.form.get('project_type')
        price = request.form.get('price')
        domain = request.form.get('domain')
        difficulty = request.form.get('difficulty')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        video_url = request.form.get('video_url')
        github_url = request.form.get('github_url')
        requirements = request.form.get('requirements')
        instructions = request.form.get('instructions')

        # Handle file uploads (in a real app, save files)
        screenshots = request.files.getlist('screenshots')
        zip_file = request.files.get('zip_file')

        # In a real app, you would save this to a database
        flash('Your project has been submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('sell_your_project.html')

@app.route('/browse_all_projects')
def browse_all_projects():
    # Get filter parameters
    categories = request.args.getlist('categories')
    project_type = request.args.get('project_type', '')
    price_range = request.args.get('price_range', '')
    difficulties = request.args.getlist('difficulty')
    sort_by = request.args.get('sort', 'popularity')

    # Filter projects
    filtered_projects = PROJECTS_DATA.copy()

    # Filter by categories
    if categories:
        tech_filters = []
        for cat in categories:
            if cat in CATEGORY_MAPPINGS:
                tech_filters.extend(CATEGORY_MAPPINGS[cat])
        if tech_filters:
            filtered_projects = [p for p in filtered_projects if any(tech in p['technology'] for tech in tech_filters)]

    # Filter by project type
    if project_type:
        if project_type == 'mini':
            filtered_projects = [p for p in filtered_projects if p['price'] < 40]
        elif project_type == 'major':
            filtered_projects = [p for p in filtered_projects if p['price'] >= 40]

    # Filter by price range
    if price_range:
        if price_range == 'under_30':
            filtered_projects = [p for p in filtered_projects if p['price'] < 30]
        elif price_range == '30_60':
            filtered_projects = [p for p in filtered_projects if 30 <= p['price'] <= 60]
        elif price_range == 'over_60':
            filtered_projects = [p for p in filtered_projects if p['price'] > 60]

    # Filter by difficulty
    if difficulties:
        difficulty_mapping = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced'
        }
        diff_filters = [difficulty_mapping.get(d, d) for d in difficulties]
        filtered_projects = [p for p in filtered_projects if p['difficulty'] in diff_filters]

    # Sort projects
    if sort_by == 'popularity':
        filtered_projects.sort(key=lambda x: (-x['popularity'], -x['sales_count']))
    elif sort_by == 'newest':
        filtered_projects.sort(key=lambda x: x['date_added'], reverse=True)
    elif sort_by == 'price-low':
        filtered_projects.sort(key=lambda x: x['price'])
    elif sort_by == 'price-high':
        filtered_projects.sort(key=lambda x: x['price'], reverse=True)

    return render_template('browse_all_projects.html', projects=filtered_projects)

@app.route('/api/filter_projects')
def api_filter_projects():
    # Get filter parameters
    categories = request.args.getlist('categories')
    project_type = request.args.get('project_type', '')
    price_range = request.args.get('price_range', '')
    difficulties = request.args.getlist('difficulty')
    sort_by = request.args.get('sort', 'popularity')

    # Filter projects
    filtered_projects = PROJECTS_DATA.copy()

    # Filter by categories
    if categories:
        tech_filters = []
        for cat in categories:
            if cat in CATEGORY_MAPPINGS:
                tech_filters.extend(CATEGORY_MAPPINGS[cat])
        if tech_filters:
            filtered_projects = [p for p in filtered_projects if any(tech in p['technology'] for tech in tech_filters)]

    # Filter by project type
    if project_type:
        if project_type == 'mini':
            filtered_projects = [p for p in filtered_projects if p['price'] < 40]
        elif project_type == 'major':
            filtered_projects = [p for p in filtered_projects if p['price'] >= 40]

    # Filter by price range
    if price_range:
        if price_range == 'under_30':
            filtered_projects = [p for p in filtered_projects if p['price'] < 30]
        elif price_range == '30_60':
            filtered_projects = [p for p in filtered_projects if 30 <= p['price'] <= 60]
        elif price_range == 'over_60':
            filtered_projects = [p for p in filtered_projects if p['price'] > 60]

    # Filter by difficulty
    if difficulties:
        difficulty_mapping = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced'
        }
        diff_filters = [difficulty_mapping.get(d, d) for d in difficulties]
        filtered_projects = [p for p in filtered_projects if p['difficulty'] in diff_filters]

    # Sort projects
    if sort_by == 'popularity':
        filtered_projects.sort(key=lambda x: (-x['popularity'], -x['sales_count']))
    elif sort_by == 'newest':
        filtered_projects.sort(key=lambda x: x['date_added'], reverse=True)
    elif sort_by == 'price-low':
        filtered_projects.sort(key=lambda x: x['price'])
    elif sort_by == 'price-high':
        filtered_projects.sort(key=lambda x: x['price'], reverse=True)

    # Calculate counts for categories
    category_counts = {}
    for cat_key, techs in CATEGORY_MAPPINGS.items():
        count = sum(1 for p in PROJECTS_DATA if any(tech in p['technology'] for tech in techs))
        category_counts[cat_key] = count

    # Project type counts
    mini_count = sum(1 for p in PROJECTS_DATA if p['price'] < 40)
    major_count = sum(1 for p in PROJECTS_DATA if p['price'] >= 40)

    return {
        'projects': filtered_projects,
        'total_count': len(filtered_projects),
        'category_counts': category_counts,
        'project_type_counts': {'mini': mini_count, 'major': major_count}
    }

@app.route('/project/<int:project_id>')
def project_details(project_id):
    # Find the project by ID
    project = next((p for p in PROJECTS_DATA if p['id'] == project_id), None)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('index'))

    return render_template('project_details.html', project=project)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('browse_all_projects'))

    # Filter projects based on search query
    filtered_projects = [
        p for p in PROJECTS_DATA
        if query in p['title'].lower() or
           query in p['description'].lower() or
           any(query in tech.lower() for tech in p['technology'])
    ]

    return render_template('browse_all_projects.html', projects=filtered_projects)

@app.route('/custom_project_request', methods=['POST'])
def custom_project_request():
    name = request.form.get('name')
    email = request.form.get('email')
    project_type = request.form.get('project_type')
    budget = request.form.get('budget')
    technologies = request.form.get('technologies')
    deadline = request.form.get('deadline')
    description = request.form.get('description')
    additional_info = request.form.get('additional_info')

    # In a real app, you would save this to a database
    flash('Your custom project request has been submitted! We will contact you soon.', 'success')
    return redirect(url_for('index'))

@app.route('/get_guidance', methods=['POST'])
def get_guidance():
    email = request.form.get('email')
    project_type = request.form.get('project_type')
    description = request.form.get('description')

    # In a real app, you would send an email or save to database
    flash('Your guidance request has been submitted! We will contact you soon.', 'success')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    # Get categories
    categories_list = [
        "Web Development",
        "Mobile App",
        "Web Application",
        "Data Science",
        "Artificial Intelligence",
        "Blockchain",
        "Cybersecurity",
        "Cloud Computing"
    ]
    return render_template('index.html', categories=categories_list)  # For now, redirect to index

@app.route('/contact')
def contact():
    return render_template('index.html')  # For now, redirect to index

@app.route('/login')
def login():
    return render_template('index.html')  # For now, redirect to index

if __name__ == '__main__':
    app.run(debug=True)