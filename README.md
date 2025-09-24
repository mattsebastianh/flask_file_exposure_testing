# 🔒 Flask File Upload & Access Security Testing

A comprehensive Flask web application designed to demonstrate secure file upload and access controls, with extensive security testing to identify and prevent common web application vulnerabilities.

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Security Implementations](#-security-implementations)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Testing Implementation](#-testing-implementation)
- [Security Tests](#-security-tests)
- [API Endpoints](#-api-endpoints)
- [Templates](#-templates)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Overview

This Flask application serves as an educational platform for understanding web application security vulnerabilities and secure coding practices. It demonstrates proper implementation of:

- **Authentication & Session Management**
- **Secure File Upload Handling**
- **Path Traversal Protection**
- **Input Validation & Sanitization**
- **Access Control Mechanisms**

### Project Goals

1. **Educational**: Demonstrate common security vulnerabilities and their mitigation
2. **Testing**: Provide comprehensive security testing framework
3. **Best Practices**: Showcase Flask security implementation patterns
4. **Documentation**: Serve as a reference for secure web development

## ✨ Features

### Core Functionality
- 🔐 **Secure Authentication System** with session management
- 📤 **File Upload** with validation and sanitization
- 📁 **File Management** (view, download, list files)
- 🛡️ **Security Headers** implementation
- 🎨 **Template-based UI** using Jinja2
- ⚡ **Flash Messaging** system for user feedback

### Security Features
- ✅ **Authentication Required** for all file operations
- ✅ **File Type Validation** (configurable allowed extensions)
- ✅ **File Size Limits** (16MB default)
- ✅ **Path Traversal Protection**
- ✅ **Filename Sanitization**
- ✅ **Security Headers** (XSS, CSRF, Clickjacking protection)
- ✅ **Input Validation** and error handling

## 🛡️ Security Implementations

| Security Measure | Implementation | Status |
|------------------|----------------|---------|
| Authentication | Session-based login system | ✅ Implemented |
| Path Traversal Protection | `is_safe_path()` validation | ✅ Implemented |
| File Type Validation | Extension whitelist | ✅ Implemented |
| File Size Limits | 16MB upload limit | ✅ Implemented |
| Filename Sanitization | `secure_filename()` usage | ✅ Implemented |
| Security Headers | XSS, CSRF, Clickjacking | ✅ Implemented |
| Input Validation | Form data validation | ✅ Implemented |
| Error Handling | Graceful error pages | ✅ Implemented |

## 📁 Project Structure

```
flask_file_exposure_testing/
├── 📄 app.py                    # Main Flask application
├── 📄 app_test.py               # Comprehensive security tests
├── 📄 README.md                 # Project documentation
├── 📄 project_brief.md          # Project overview
├── 📄 .gitignore               # Git ignore rules
├── 📁 templates/               # HTML templates
│   ├── 📄 login.html           # Login page template
│   ├── 📄 index.html           # Dashboard template
│   ├── 📄 list_files.html      # File listing template
│   ├── 📄 view_file.html       # File viewer template
│   ├── 📄 error.html           # Error page template
│   └── 📄 cannot_view_file.html # File type error template
├── 📁 uploaded_files/          # User uploaded files storage
├── 📁 files_to_upload/         # Sample files for testing
├── 📁 reports/                 # Security reports and documentation
└── 📁 __pycache__/             # Python cache files
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Flask 2.0+
- Werkzeug (included with Flask)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask_file_exposure_testing
   ```

2. **Install dependencies**
   ```bash
   pip install flask werkzeug
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open browser to `http://localhost:5000`
   - Use demo credentials: `admin` / `secure_password_123`

## 💻 Usage

### Starting the Application
```bash
python app.py
```

### Demo Credentials
- **Username**: `admin`
- **Password**: `secure_password_123`

### Basic Workflow
1. **Login** using demo credentials
2. **Upload Files** through the secure upload form
3. **View Files** in the file management section
4. **Download/View** uploaded files
5. **Logout** when finished

## 🧪 Testing Implementation

The project includes comprehensive security testing through `app_test.py` using Python's unittest framework.

### Test Categories

#### 1. Authentication Tests
```python
def test_authentication_system(self):
    """Test the authentication system security"""
    - Invalid credentials rejection
    - Valid credentials acceptance  
    - Protected route access control
```

#### 2. Path Traversal Tests
```python
def test_path_traversal_vulnerability(self):
    """Test path traversal attack prevention"""
    - Unauthenticated access blocking
    - Authenticated path traversal prevention
    - System file access protection
```

#### 3. File Upload Tests
```python
def test_file_upload_vulnerability(self):
    """Test file upload security measures"""
    - Unauthenticated upload blocking
    - Malicious file type rejection
    - Valid file upload processing
```

#### 4. File Access Tests
```python
def test_direct_file_access_vulnerability(self):
    """Test file access control mechanisms"""
    - Protected file access control
    - System file protection
    - Authenticated vs unauthenticated access
```

### Running Tests

**Execute all security tests:**
```bash
python app_test.py
```

**Run specific test:**
```bash
python -m unittest app_test.TestFlaskApp.test_path_traversal_vulnerability
```

### Expected Test Output
```
=== AUTHENTICATION SECURITY TEST ===
Invalid login test - Status: 200
✅ SECURE: Invalid credentials properly rejected
Valid login test - Status: 200
✅ SECURE: Valid credentials accepted
✅ SECURE: Protected routes accessible after authentication

=== COMPREHENSIVE SECURITY TEST ===
Unauthenticated access to protected file - Status: 302
✅ SECURE: Unauthenticated access properly blocked
✅ SECURE: System file ../app.py access blocked
✅ SECURE: System file ../../etc/passwd access blocked
✅ OVERALL: All system file access properly blocked
```

## 🔍 Security Tests

| Test Name | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_authentication_system` | Validates login/logout functionality | ✅ Pass |
| `test_path_traversal_vulnerability` | Tests directory traversal attacks | ✅ Pass |
| `test_file_upload_vulnerability` | Tests malicious file upload prevention | ✅ Pass |
| `test_direct_file_access_vulnerability` | Tests unauthorized file access | ✅ Pass |
| `test_access_to_protected_files` | Comprehensive file access testing | ✅ Pass |

### Security Test Coverage

- **Authentication Bypass**: ❌ Prevented
- **Path Traversal**: ❌ Prevented  
- **File Type Validation**: ✅ Enforced
- **Size Limit Enforcement**: ✅ Enforced
- **Unauthorized Access**: ❌ Prevented
- **Session Management**: ✅ Secure

## 🌐 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | ✅ Yes | Dashboard/home page |
| `/login` | GET, POST | ❌ No | User authentication |
| `/logout` | GET | ✅ Yes | User logout |
| `/upload` | POST | ✅ Yes | File upload handler |
| `/list-files` | GET | ✅ Yes | List uploaded files |
| `/files/<filename>` | GET | ✅ Yes | Download file |
| `/view/<filename>` | GET | ✅ Yes | View file content |

## 🎨 Templates

The application uses Jinja2 templating with the following structure:

| Template | Purpose | Features |
|----------|---------|----------|
| `login.html` | User authentication | Demo credentials display, flash messages |
| `index.html` | Main dashboard | File upload form, security info |
| `list_files.html` | File listing | Dynamic file list, download/view links |
| `view_file.html` | File content viewer | Text file content display |
| `error.html` | Generic error page | Customizable error messages |
| `cannot_view_file.html` | File type error | Non-text file handling |

## ⚙️ Configuration

### Security Configuration
```python
# File upload settings
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Authentication credentials
VALID_CREDENTIALS = {
    'admin': 'secure_password_123'
}

# Security headers
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_APP`: Set to `app.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/security-improvement`)
3. Commit your changes (`git commit -am 'Add new security feature'`)
4. Push to the branch (`git push origin feature/security-improvement`)
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add security tests for new features
- Update documentation for API changes
- Ensure all security tests pass

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 mattsebash

## 🔗 Additional Resources

- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.0.x/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Secure File Upload Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

---

**⚠️ Security Notice**: This application is designed for educational purposes. Always implement additional security measures in production environments.