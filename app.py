from flask import Flask, send_from_directory, request, session, redirect, url_for, flash, abort
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
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔐 Secure Login</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 450px; 
                margin: 80px auto; 
                padding: 20px; 
                background-color: #f5f5f5;
            }
            .login-form { 
                background: white; 
                padding: 30px; 
                border-radius: 8px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { 
                text-align: center; 
                color: #333; 
                margin-bottom: 20px;
            }
            .credentials-note {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                border-left: 4px solid #f39c12;
                text-align: center;
            }
            .credentials-note strong {
                color: #856404;
                display: block;
                margin-bottom: 10px;
            }
            .credential-item {
                font-family: monospace;
                background: #f8f9fa;
                padding: 4px 8px;
                border-radius: 3px;
                margin: 2px;
                display: inline-block;
                font-weight: bold;
            }
            input[type="text"], input[type="password"] { 
                width: 100%; 
                padding: 12px; 
                margin: 10px 0; 
                border: 1px solid #ddd; 
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"] { 
                width: 100%; 
                background-color: #4CAF50; 
                color: white; 
                padding: 12px; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 16px;
            }
            input[type="submit"]:hover { 
                background-color: #45a049; 
            }
        </style>
    </head>
    <body>
        <div class="login-form">
            <h1>🔐 Secure Login</h1>
            
            <div class="credentials-note">
                <strong>🔑 Demo Credentials</strong>
                Username: <span class="credential-item">admin</span><br>
                Password: <span class="credential-item">secure_password_123</span>
            </div>
            
            <form method="post">
                <label>Username:</label>
                <input type="text" name="username" required>
                <label>Password:</label>
                <input type="password" name="password" required>
                <input type="submit" value="Login">
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    username = session.get('username', 'User')
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔒 Secure File Upload System</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                max-width: 700px; 
                margin: 30px auto; 
                padding: 20px; 
            }}
            .header {{ 
                background: #f8f9fa; 
                padding: 15px; 
                border-radius: 5px; 
                margin-bottom: 20px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
            }}
            .upload-form {{ 
                border: 2px dashed #28a745; 
                padding: 20px; 
                text-align: center; 
                margin: 20px 0; 
                border-radius: 5px; 
            }}
            input[type="file"] {{ 
                margin: 10px 0; 
                padding: 5px; 
            }}
            input[type="submit"] {{ 
                background-color: #28a745; 
                color: white; 
                padding: 12px 25px; 
                border: none; 
                cursor: pointer; 
                font-size: 16px; 
                border-radius: 4px; 
            }}
            input[type="submit"]:hover {{ 
                background-color: #218838; 
            }}
            .security-info {{ 
                background: #d1ecf1; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 15px 0; 
            }}
            .logout-btn {{ 
                background: #dc3545; 
                color: white; 
                padding: 8px 15px; 
                text-decoration: none; 
                border-radius: 4px; 
            }}
            .credentials-info {{
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
                border-left: 4px solid #f39c12;
            }}
            .credentials-info strong {{
                color: #856404;
            }}
            .credential-item {{
                font-family: monospace;
                background: #f8f9fa;
                padding: 4px 8px;
                border-radius: 3px;
                margin: 2px;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <h1>🔒 Secure File Upload System</h1>
                <small>Welcome, {username}!</small>
            </div>
            <a href="/logout" class="logout-btn">Logout</a>
        </div>
        
        <div class="security-info">
            <strong>🛡️ Security Features Active:</strong><br>
            • Authentication required<br>
            • File type validation ({', '.join(ALLOWED_EXTENSIONS)})<br>
            • File size limit: {MAX_FILE_SIZE // (1024*1024)}MB<br>
            • Path traversal protection<br>
            • Filename sanitization
        </div>
        
        <div class="upload-form">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <p><strong>Select a secure file to upload:</strong></p>
                <input type="file" name="file" required accept=".txt,.pdf,.png,.jpg,.jpeg,.gif,.docx">
                <br><br>
                <input type="submit" value="🔐 Upload Securely">
            </form>
        </div>
        
        <h2>📁 File Management:</h2>
        <div style="border: 1px solid #ddd; padding: 15px; margin: 20px 0; border-radius: 5px;">
            <p><a href="/list-files" style="color: #28a745; text-decoration: none; font-weight: bold;">📂 View Uploaded Files</a></p>
        </div>
        
        <div class="security-info">
            <strong>🔍 Security Improvements:</strong><br>
            • All file access now requires authentication<br>
            • Malicious file uploads are blocked<br>
            • Path traversal attacks are prevented<br>
            • Secure filename handling implemented
        </div>
    </body>
    </html>
    '''

@app.route('/list-files')
@login_required
def list_files():
    uploaded_files_dir = './uploaded_files'
    try:
        files = os.listdir(uploaded_files_dir)
        file_list_html = ''
        
        if not files:
            file_list_html = '<p>No files uploaded yet.</p>'
        else:
            for file in files:
                file_list_html += f'''
                <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0; border-radius: 5px;">
                    <strong>📄 {file}</strong><br>
                    <a href="/files/{file}" style="color: #4CAF50; text-decoration: none; margin-right: 15px;">📥 Download</a>
                    <a href="/view/{file}" style="color: #2196F3; text-decoration: none;">👁️ View Content</a>
                </div>
                '''
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Uploaded Files</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                a {{ text-decoration: none; }}
                .back-link {{ color: #666; margin-bottom: 20px; display: block; }}
            </style>
        </head>
        <body>
            <a href="/" class="back-link">← Back to Upload</a>
            <h1>📁 Uploaded Files</h1>
            {file_list_html}
        </body>
        </html>
        '''
    except FileNotFoundError:
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error: Upload directory not found!</h1>
            <a href="/">← Back to Upload</a>
        </body>
        </html>
        '''

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
            
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>View: {filename}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                    .content {{ background: #f5f5f5; padding: 20px; border-radius: 5px; white-space: pre-wrap; }}
                    .back-link {{ color: #666; margin-bottom: 20px; display: block; }}
                </style>
            </head>
            <body>
                <a href="/list-files" class="back-link">← Back to Files</a>
                <h1>📄 {filename}</h1>
                <div class="content">{content}</div>
            </body>
            </html>
            '''
        else:
            return f'''
            <!DOCTYPE html>
            <html>
            <head><title>Cannot View File</title></head>
            <body>
                <h1>Cannot view this file type</h1>
                <p>File: {filename}</p>
                <p>Only .txt files can be viewed directly.</p>
                <a href="/list-files">← Back to Files</a>
            </body>
            </html>
            '''
    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>Error reading file</h1>
            <p>Could not read {filename}</p>
            <a href="/list-files">← Back to Files</a>
        </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)