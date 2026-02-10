import requests
import sys
from datetime import datetime

class SocialMediaAPITester:
    def __init__(self, base_url="https://site-creator-913.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.status_code == 200:
                    try:
                        json_data = response.json()
                        if isinstance(json_data, list):
                            print(f"   Response: List with {len(json_data)} items")
                        else:
                            print(f"   Response: {type(json_data).__name__}")
                    except:
                        print(f"   Response: Non-JSON")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.status_code != expected_status:
                    print(f"   Response body: {response.text[:200]}...")

            return success, response.json() if success and response.status_code == 200 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        success, response = self.run_test(
            "API Root",
            "GET",
            "",
            200
        )
        return success

    def test_visual_styles(self):
        """Test visual styles endpoint"""
        success, response = self.run_test(
            "Visual Styles",
            "GET", 
            "visual-styles",
            200
        )
        
        if success and response:
            print(f"   Found {len(response)} visual styles")
            # Test structure of first style
            if len(response) > 0:
                style = response[0]
                required_fields = ['id', 'title', 'images']
                has_all_fields = all(field in style for field in required_fields)
                print(f"   First style has required fields: {has_all_fields}")
                if 'images' in style and isinstance(style['images'], list):
                    print(f"   First style has {len(style['images'])} images")
        
        return success

    def test_hooks(self):
        """Test hooks endpoint"""
        success, response = self.run_test(
            "All Hooks",
            "GET",
            "hooks", 
            200
        )
        
        if success and response:
            print(f"   Found {len(response)} hooks")
            # Test categories
            categories = set()
            for hook in response:
                if 'category' in hook:
                    categories.add(hook['category'])
            print(f"   Categories found: {list(categories)}")
            
            # Test structure
            if len(response) > 0:
                hook = response[0]
                required_fields = ['id', 'category', 'idea']
                has_all_fields = all(field in hook for field in required_fields)
                print(f"   First hook has required fields: {has_all_fields}")
        
        return success

    def test_scripts(self):
        """Test scripts endpoint"""
        success, response = self.run_test(
            "All Scripts",
            "GET",
            "scripts",
            200
        )
        
        if success and response:
            print(f"   Found {len(response)} scripts")
            # Test types
            types = set()
            for script in response:
                if 'type' in script:
                    types.add(script['type'])
            print(f"   Script types found: {list(types)}")
            
            # Count by type
            other_count = sum(1 for s in response if s.get('type') == 'other')
            engagement_count = sum(1 for s in response if s.get('type') == 'engagement')
            print(f"   Other scripts: {other_count}, Engagement scripts: {engagement_count}")
            
            # Test structure
            if len(response) > 0:
                script = response[0]
                required_fields = ['id', 'type', 'paragraph1', 'paragraph2']
                has_all_fields = all(field in script for field in required_fields)
                print(f"   First script has required fields: {has_all_fields}")
        
        return success

    def test_status_endpoint(self):
        """Test status check endpoints"""
        # Test POST
        test_data = {
            "client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"
        }
        
        success_post, response_post = self.run_test(
            "Status Check POST",
            "POST",
            "status",
            200,
            data=test_data
        )
        
        if not success_post:
            return False
            
        # Test GET
        success_get, response_get = self.run_test(
            "Status Check GET",
            "GET",
            "status",
            200
        )
        
        if success_get and response_get:
            print(f"   Found {len(response_get)} status checks")
        
        return success_get

def main():
    print("🚀 Starting Social Media Content Creator API Tests")
    print("=" * 60)
    
    # Setup
    tester = SocialMediaAPITester()
    
    # Run core content tests
    tests = [
        tester.test_api_root,
        tester.test_visual_styles, 
        tester.test_hooks,
        tester.test_scripts,
        tester.test_status_endpoint
    ]
    
    failed_tests = []
    
    for test in tests:
        try:
            if not test():
                failed_tests.append(test.__name__)
        except Exception as e:
            print(f"❌ Exception in {test.__name__}: {str(e)}")
            failed_tests.append(test.__name__)
    
    # Print results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if failed_tests:
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
        return 1
    else:
        print("✅ All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())