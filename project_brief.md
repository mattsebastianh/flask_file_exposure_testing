# Project Name: **Flask File Upload & Access Security Testing**

## Project Brief

This project consists of a simple Flask web application that provides endpoints for file uploads and serving files from a directory. It highlights potential vulnerabilities such as path traversal and improper file access, emphasizing the importance of secure coding practices.

The accompanying unit tests are designed to assess the application's security by checking for:

1. **Path Traversal Vulnerabilities**: Testing if malicious input can retrieve source code or unwanted files.
2. **Direct File Access**: Ensuring sensitive files are not accessible through the application.
3. **File Upload Validations**: Checking for secure handling of uploaded files to prevent unauthorized access.
4. **Access Control**: Verifying that protected files cannot be accessed by unauthorized users.

This project aims to serve as an educational tool for understanding web application security vulnerabilities and advocating for secure coding techniques in Flask applications.
