"""Simple web-based testing UI using Python's built-in HTTP server.

Run with: python -m src.test_ui.web
"""

import asyncio
import html
import http.server
import json
import socketserver
import urllib.parse
from datetime import date
from typing import Any

PORT = 8080


class TestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for the testing UI."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/" or self.path == "/index.html":
            self.send_html_response(self.get_main_page())
        elif self.path == "/api/modules":
            self.send_json_response(self.get_modules_info())
        elif self.path == "/api/run-tests":
            self.send_json_response(self.run_tests())
        elif self.path.startswith("/api/test-module/"):
            module_name = self.path.split("/")[-1]
            self.send_json_response(self.test_module(module_name))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        if self.path == "/api/create-student":
            data = json.loads(post_data) if post_data else {}
            result = asyncio.run(self.create_test_student(data))
            self.send_json_response(result)
        else:
            self.send_error(404, "Not Found")

    def send_html_response(self, content: str):
        """Send HTML response."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def send_json_response(self, data: Any):
        """Send JSON response."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def get_modules_info(self) -> list:
        """Get information about all modules."""
        return [
            {
                "name": "StudentProfileModule",
                "display_name": "Student Profile & Assessment",
                "description": "Comprehensive student profiling, assessment, and goal-setting system",
                "test_file": "test_profile.py",
            },
            {
                "name": "AcademicPlanningModule",
                "display_name": "Academic Planning",
                "description": "Course selection, GPA planning, and academic trajectory optimization",
                "test_file": "test_academic.py",
            },
            {
                "name": "ExtracurricularAdvisorModule",
                "display_name": "Extracurricular Advisor",
                "description": "Activity recommendations and competition matching",
                "test_file": "test_all_modules.py",
            },
            {
                "name": "SummerProgramsModule",
                "display_name": "Summer Programs",
                "description": "Summer program and opportunity matching",
                "test_file": "test_all_modules.py",
            },
            {
                "name": "CollegeResearchModule",
                "display_name": "College Research",
                "description": "College matching and admission analysis",
                "test_file": "test_all_modules.py",
            },
            {
                "name": "EssayWorkshopModule",
                "display_name": "Essay Workshop",
                "description": "Essay development, feedback, and revision support",
                "test_file": "test_essay.py",
            },
            {
                "name": "ApplicationManagerModule",
                "display_name": "Application Manager",
                "description": "Application tracking and submission management",
                "test_file": "test_all_modules.py",
            },
            {
                "name": "TimelineOrchestratorModule",
                "display_name": "Timeline Orchestrator",
                "description": "Timeline and milestone management",
                "test_file": "test_all_modules.py",
            },
        ]

    def run_tests(self) -> dict:
        """Run pytest and return results."""
        import subprocess

        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd="/home/user/huilingding",
                timeout=60,
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Tests timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def test_module(self, module_name: str) -> dict:
        """Test a specific module."""
        import subprocess

        test_file_map = {
            "profile": "tests/test_modules/test_profile.py",
            "academic": "tests/test_modules/test_academic.py",
            "essay": "tests/test_modules/test_essay.py",
            "core": "tests/test_core/",
            "all": "tests/test_modules/test_all_modules.py",
        }

        test_path = test_file_map.get(module_name, f"tests/test_modules/test_{module_name}.py")

        try:
            result = subprocess.run(
                ["python", "-m", "pytest", test_path, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd="/home/user/huilingding",
                timeout=30,
            )
            return {
                "module": module_name,
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
            }
        except Exception as e:
            return {"module": module_name, "success": False, "error": str(e)}

    async def create_test_student(self, data: dict) -> dict:
        """Create a test student using the profile module."""
        from src.modules.profile import StudentProfileModule

        # Use mock AI engine
        class MockEngine:
            async def generate_text(self, *args, **kwargs):
                return "Mock response"

            async def generate_structured(self, *args, **kwargs):
                raise NotImplementedError()

            async def analyze_essay(self, *args, **kwargs):
                return {}

            async def chat(self, *args, **kwargs):
                return "Mock chat"

        try:
            module = StudentProfileModule(MockEngine())

            student = await module.create_profile(
                first_name=data.get("first_name", "Test"),
                last_name=data.get("last_name", "Student"),
                email=data.get("email", "test@example.com"),
                date_of_birth=date(2008, 1, 1),
                high_school=data.get("high_school", "Test High School"),
                graduation_year=int(data.get("graduation_year", 2026)),
                state=data.get("state", "CA"),
            )

            return {
                "success": True,
                "student": {
                    "id": student.id,
                    "name": student.personal_info.full_name,
                    "school": student.personal_info.high_school,
                    "graduation_year": student.personal_info.graduation_year,
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_main_page(self) -> str:
        """Generate the main HTML page."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI College Planner - Module Testing UI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5em;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .card h2 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .module-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }
        .module-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: transform 0.2s, border-color 0.2s;
        }
        .module-card:hover {
            transform: translateY(-3px);
            border-color: #00d4ff;
        }
        .module-card h3 {
            color: #fff;
            font-size: 1.1em;
            margin-bottom: 8px;
        }
        .module-card p {
            color: #aaa;
            font-size: 0.9em;
            margin-bottom: 12px;
        }
        button {
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9em;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .output {
            background: #0d1117;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.85em;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .success { color: #3fb950; }
        .error { color: #f85149; }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #aaa;
        }
        .form-group input {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .status-pass { background: #238636; }
        .status-fail { background: #da3633; }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #00d4ff;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI College Planner - Module Testing</h1>

        <div class="card">
            <h2>Quick Actions</h2>
            <button onclick="runAllTests()">Run All Tests</button>
            <button onclick="loadModules()" class="btn-secondary">Refresh Modules</button>
        </div>

        <div class="card">
            <h2>Available Modules</h2>
            <div id="modules" class="module-grid">Loading...</div>
        </div>

        <div class="card">
            <h2>Test Output</h2>
            <div id="output" class="output">Click "Run All Tests" or test a specific module to see results.</div>
        </div>

        <div class="card">
            <h2>Interactive Test: Create Student Profile</h2>
            <form id="studentForm" onsubmit="createStudent(event)">
                <div class="form-row">
                    <div class="form-group">
                        <label for="firstName">First Name</label>
                        <input type="text" id="firstName" value="Jane" required>
                    </div>
                    <div class="form-group">
                        <label for="lastName">Last Name</label>
                        <input type="text" id="lastName" value="Doe" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" value="jane.doe@example.com" required>
                    </div>
                    <div class="form-group">
                        <label for="highSchool">High School</label>
                        <input type="text" id="highSchool" value="Springfield High" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="gradYear">Graduation Year</label>
                        <input type="number" id="gradYear" value="2026" required>
                    </div>
                    <div class="form-group">
                        <label for="state">State</label>
                        <input type="text" id="state" value="CA" required>
                    </div>
                </div>
                <button type="submit">Create Student Profile</button>
            </form>
            <div id="studentResult" class="output" style="margin-top: 15px;"></div>
        </div>
    </div>

    <script>
        async function loadModules() {
            const container = document.getElementById('modules');
            try {
                const response = await fetch('/api/modules');
                const modules = await response.json();
                container.innerHTML = modules.map(m => `
                    <div class="module-card">
                        <h3>${m.display_name}</h3>
                        <p>${m.description}</p>
                        <button onclick="testModule('${m.name.toLowerCase().replace('module', '')}')">
                            Test Module
                        </button>
                    </div>
                `).join('');
            } catch (e) {
                container.innerHTML = '<p class="error">Failed to load modules</p>';
            }
        }

        async function runAllTests() {
            const output = document.getElementById('output');
            output.innerHTML = '<span class="loading"></span> Running all tests...';
            try {
                const response = await fetch('/api/run-tests');
                const result = await response.json();
                output.innerHTML = result.success
                    ? `<span class="success">All tests passed!</span>\\n\\n${result.output}`
                    : `<span class="error">Some tests failed</span>\\n\\n${result.output}\\n${result.errors}`;
            } catch (e) {
                output.innerHTML = `<span class="error">Error: ${e.message}</span>`;
            }
        }

        async function testModule(name) {
            const output = document.getElementById('output');
            output.innerHTML = `<span class="loading"></span> Testing ${name} module...`;
            try {
                const response = await fetch(`/api/test-module/${name}`);
                const result = await response.json();
                output.innerHTML = result.success
                    ? `<span class="success">${name} tests passed!</span>\\n\\n${result.output}`
                    : `<span class="error">${name} tests failed</span>\\n\\n${result.output}\\n${result.errors || ''}`;
            } catch (e) {
                output.innerHTML = `<span class="error">Error: ${e.message}</span>`;
            }
        }

        async function createStudent(event) {
            event.preventDefault();
            const result = document.getElementById('studentResult');
            result.innerHTML = '<span class="loading"></span> Creating student...';

            const data = {
                first_name: document.getElementById('firstName').value,
                last_name: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                high_school: document.getElementById('highSchool').value,
                graduation_year: document.getElementById('gradYear').value,
                state: document.getElementById('state').value,
            };

            try {
                const response = await fetch('/api/create-student', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
                const res = await response.json();
                if (res.success) {
                    result.innerHTML = `<span class="success">Student created successfully!</span>
ID: ${res.student.id}
Name: ${res.student.name}
School: ${res.student.school}
Graduation: ${res.student.graduation_year}`;
                } else {
                    result.innerHTML = `<span class="error">Error: ${res.error}</span>`;
                }
            } catch (e) {
                result.innerHTML = `<span class="error">Error: ${e.message}</span>`;
            }
        }

        // Load modules on page load
        loadModules();
    </script>
</body>
</html>"""


def main():
    """Start the web server."""
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Module Testing UI running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    main()
