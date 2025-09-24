from flask import Flask, send_from_directory, request, session, redirect, url_for, flash, abort, render_template
import os
import secrets
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response

# File upload configuration
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB limit
UPLOAD_FOLDER = './uploaded_files'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Authentication credentials
VALID_CREDENTIALS = {
    'admin': 'secure_password_123'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_path(basedir, path, follow_symlinks=True):
    if follow_symlinks:
        matchpath = os.path.realpath(path)
    else:
        matchpath = os.path.abspath(path)
    return basedir == os.path.commonpath((basedir, matchpath))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    username = session.get('username', 'User')
    
    # Prepare template variables
    allowed_extensions = list(ALLOWED_EXTENSIONS)
    max_file_size_mb = MAX_FILE_SIZE // (1024*1024)
    file_accept_types = '.' + ',.'.join(ALLOWED_EXTENSIONS)
    
    return render_template('index.html',
                         username=username,
                         allowed_extensions=allowed_extensions,
                         max_file_size_mb=max_file_size_mb,
                         file_accept_types=file_accept_types)

@app.route('/list-files')
@login_required
def list_files():
    uploaded_files_dir = './uploaded_files'
    try:
        files = os.listdir(uploaded_files_dir)
        return render_template('list_files.html', files=files)
    except FileNotFoundError:
        return render_template('error.html',
                             error_title='Error: Upload directory not found!',
                             error_message='The upload directory could not be found.',
                             back_url='/',
                             back_text='Back to Upload')

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        flash(f'File too large! Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        if '/' in filename or '\\\\' in filename:
            flash('Invalid filename!', 'error')
            return redirect(url_for('index'))
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not is_safe_path(os.path.abspath(UPLOAD_FOLDER), os.path.abspath(file_path)):
            flash('Invalid file path!', 'error')
            return redirect(url_for('index'))
        
        file.save(file_path)
        flash(f'File {filename} uploaded successfully!', 'success')
        return redirect(url_for('index'))
    else:
        flash('File type not allowed!', 'error')
        return redirect(url_for('index'))

@app.route('/files/<filename>')
@login_required
def uploaded_file(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(os.path.abspath(UPLOAD_FOLDER), filename)
    
    if not is_safe_path(os.path.abspath(UPLOAD_FOLDER), file_path):
        abort(404)
    
    if not os.path.exists(file_path):
        abort(404)
    
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/view/<filename>')
@login_required
def view_file_content(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(os.path.abspath(UPLOAD_FOLDER), filename)
    
    if not is_safe_path(os.path.abspath(UPLOAD_FOLDER), file_path):
        abort(404)
    
    if not os.path.exists(file_path):
        abort(404)
    
    try:
        if filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return render_template('view_file.html', filename=filename, content=content)
        else:
            return render_template('cannot_view_file.html', filename=filename)
    except Exception as e:
        return render_template('error.html',
                             error_title='Error reading file',
                             error_message=f'Could not read {filename}',
                             back_url='/list-files',
                             back_text='Back to Files')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)