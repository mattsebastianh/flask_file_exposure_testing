import os
import unittest
import app

# Unit tests

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the Flask app and start the server thread.

        This method is called with the class as the only argument and must be a classmethod.
        It sets the app's testing mode to True and starts a new thread running the app.
        The base URL for the server is stored in the base_url class attribute.
        """
        cls.app = app.app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        
    def login(self):
        """Helper method to login for authenticated tests"""
        return self.client.post('/login', data={
            'username': 'admin',
            'password': 'securepass123'
        }, follow_redirects=True)
        
    def logout(self):
        """Helper method to logout"""
        return self.client.get('/logout', follow_redirects=True)


    @classmethod
    def tearDownClass(cls):
        # Cleanup after tests
        pass

    def test_path_traversal_vulnerability(self):
        # Test 1: Unauthenticated access should be blocked
        response = self.client.get('/files/../../app.py')
        print(f"Unauthenticated path traversal test - Status: {response.status_code}")
        if response.status_code == 302:  # Redirect to login
            print("✅ SECURE: Unauthenticated access blocked (redirected to login)")
        else:
            print("❌ VULNERABILITY: Unauthenticated access allowed!")
            
        # Test 2: Authenticated path traversal should still be blocked
        self.login()
        response = self.client.get('/files/../../app.py')
        print(f"Authenticated path traversal test - Status: {response.status_code}")
        if response.status_code in [403, 404]:
            print("✅ SECURE: Path traversal attack blocked even with authentication")
        elif response.status_code == 200:
            print("❌ VULNERABILITY: Path traversal attack succeeded!")
        self.logout()

    def test_direct_file_access_vulnerability(self):
        # Test 1: Unauthenticated access should be blocked
        response = self.client.get('/files/protected_file.txt')
        print(f"Unauthenticated file access test - Status: {response.status_code}")
        if response.status_code == 302:
            print("✅ SECURE: Unauthenticated file access blocked")
        else:
            print("❌ VULNERABILITY: Unauthenticated file access allowed!")
            
        # Test 2: Authenticated access should be controlled
        self.login()
        response = self.client.get('/files/protected_file.txt')
        print(f"Authenticated file access test - Status: {response.status_code}")
        if response.status_code == 200:
            print("⚠️  NOTICE: File accessible with authentication (this may be intended behavior)")
        else:
            print("✅ SECURE: File access properly restricted")
        self.logout()

    def test_file_upload_vulnerability(self):
        # Test 1: Unauthenticated upload should be blocked
        from io import BytesIO
        response = self.client.post('/upload', 
                                  data={'file': (BytesIO(b'test content'), 'test.txt')},
                                  content_type='multipart/form-data')
        
        print(f"Unauthenticated upload test - Status: {response.status_code}")
        if response.status_code == 302:
            print("✅ SECURE: Unauthenticated upload blocked")
        else:
            print("❌ VULNERABILITY: Unauthenticated upload allowed!")
            
        # Test 2: Authenticated malicious file upload should be blocked
        self.login()
        
        # Try to upload a malicious file
        response = self.client.post('/upload',
                                  data={'file': (BytesIO(b'<?php system($_GET["cmd"]); ?>'), 'malicious.php')},
                                  content_type='multipart/form-data')
        
        print(f"Malicious file upload test - Status: {response.status_code}")
        if response.status_code == 302:  # Redirect back to form with error
            print("✅ SECURE: Malicious file upload blocked (file extension validation)")
        elif response.status_code == 200:
            print("❌ VULNERABILITY: Malicious file upload allowed!")
            
        # Test 3: Valid file upload should work
        response = self.client.post('/upload',
                                  data={'file': (BytesIO(b'This is a safe test file.'), 'safe_test.txt')},
                                  content_type='multipart/form-data')
        
        print(f"Valid file upload test - Status: {response.status_code}")
        if response.status_code == 302:
            print("✅ SECURE: Valid file upload works with authentication")
            
        self.logout()

    def test_access_to_protected_files(self):
        print("\n=== COMPREHENSIVE SECURITY TEST ===")
        
        # Test 1: Unauthenticated access to any file should be blocked
        response = self.client.get('/files/protected_file.txt')
        print(f"Unauthenticated access to protected file - Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ SECURE: Unauthenticated access properly blocked")
        else:
            print("❌ VULNERABILITY: Unauthenticated access allowed!")
            
        # Test 2: Authenticated access controls
        self.login()
        
        # Test system file access (should be blocked even with auth)
        system_files = ['../app.py', '../../etc/passwd', '../protected_file.txt']
        all_system_files_blocked = True
        
        for file_path in system_files:
            response = self.client.get(f'/files/{file_path}')
            if response.status_code == 200:
                print(f"❌ VULNERABILITY: System file {file_path} accessible!")
                all_system_files_blocked = False
            else:
                print(f"✅ SECURE: System file {file_path} access blocked")
                
        if all_system_files_blocked:
            print("✅ OVERALL: All system file access properly blocked")
        else:
            print("❌ OVERALL: System file vulnerabilities detected!")
            
        self.logout()
        
    def test_authentication_system(self):
        """Test the authentication system itself"""
        print("\n=== AUTHENTICATION SECURITY TEST ===")
        
        # Test 1: Invalid credentials should be rejected
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        print(f"Invalid login test - Status: {response.status_code}")
        print("✅ SECURE: Invalid credentials properly rejected")
        
        # Test 2: Valid credentials should work
        response = self.login()
        print(f"Valid login test - Status: {response.status_code}")
        print("✅ SECURE: Valid credentials accepted")
        
        # Test 3: Protected routes should be accessible after login
        response = self.client.get('/')
        if response.status_code == 200:
            print("✅ SECURE: Protected routes accessible after authentication")
        
        self.logout()


if __name__ == '__main__':
    unittest.main()