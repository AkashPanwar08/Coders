from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import current_user
import requests
from app.codes import languages
from app.models import Admin, Problems

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@main.route('/home')
def index():
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        return render_template('index.html')
    return render_template('admin-home.html', active1='active')


@main.route('/home-admin', methods=['Get', 'POST'])
def homeAdmin():
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    return render_template('admin-home.html')


@main.route('/about')
def about():
    return render_template('about.html', active2='active')

@main.route('/detail<int:id>')
def detail(id):
    value = requests.get('https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=5a27d18059f749098ccbc7d4d3611f4f')
    data = value.json()
    return render_template('news-details.html', title=data['articles'][id]['title'], 
                                                date=data['articles'][id]['publishedAt'][:10],
                                                author=data['articles'][id]['author'],
                                                description=data['articles'][id]['content'],
                                                url_img=data['articles'][id]['urlToImage'],
                                                active4='active')

@main.route('/news')
def news():
    return render_template('news.html', active4='active')

@main.route('/contact')
def contact():
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('main.index'))
    return render_template('contact.html', active5='active')

@main.route('/editor-<int:prblm_id>')
def editor(prblm_id):
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('main.index'))
    problem=Problems.query.filter_by(id=prblm_id).first()
    return render_template('editor.html', languages=languages, problem=problem, id=current_user.id)
