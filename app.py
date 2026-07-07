import http.server
import json
import os
from string import Template

PORT = 5000

def load_json_data():
    if not os.path.exists('resume.json'):
        return {}
    with open('resume.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def build_resume_html(data):
    with open('templates/resume_template.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 1. Contact Links
    links_html = f"<span>📍 {data['basics'].get('location', '')}</span>"
    if data['basics'].get('phone'): links_html += f" <span>📞 {data['basics']['phone']}</span>"
    if data['basics'].get('email'): links_html += f" <span>✉️ <a href='mailto:{data['basics']['email']}'>{data['basics']['email']}</a></span>"
    for link in data['basics'].get('links', []):
        links_html += f" <span>🎨 <a href='{link.get('url', '#')}' target='_blank'>{link.get('label', 'Link')}</a></span>"

    # 2. Skills
    skills_html = ""
    for cat in data.get('skills_categories', []):
        skills_html += f"""<div class="skills-column"><ul><li><strong>{cat.get('category', 'Skills')}:</strong> {", ".join(cat.get('items', []))}</li></ul></div>"""

    # 3. Experience
    exp_html = ""
    for exp in data.get('experience', []):
        exp_html += f"""
        <div class="project-block">
            <div class="project-header">
                <div class="project-meta-left">
                    <span class="project-title">{exp.get('company', '')}</span> — <span class="project-role">{exp.get('role', '')}</span>
                </div>
                <div class="project-date">{exp.get('timeline', '')}</div>
            </div>
            <p style="font-size: 13.5px;">{exp.get('details', '')}</p>
        </div>"""

    # 4. Education Timeline
    edu_html = ""
    for edu in data.get('education_timeline', []):
        edu_html += f"""
        <div class="project-block">
            <div class="project-header">
                <div class="project-meta-left">
                    <span class="project-title">{edu.get('institution', '')}</span><br>
                    <span class="project-role" style="font-style: normal; color: var(--text-dark);">{edu.get('degree', '')}</span>
                </div>
                <div class="project-date">{edu.get('timeline', '')}</div>
            </div>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: -3px;">{edu.get('location', '')}</div>
        </div>"""

    # 5. Projects
    project_html = ""
    for proj in data.get('projects', []):
        highlights = "".join([f"<li>{h}</li>" for h in proj.get('highlights', [])])
        project_html += f"""
        <div class="project-block">
            <div class="project-header">
                <div class="project-meta-left">
                    <span class="project-title">{proj.get('name', '')}</span> — <span class="project-role">{proj.get('role', '')}</span>
                </div>
                <div class="project-date">{proj.get('context', '')}</div>
            </div>
            <p style="margin-bottom: 5px; font-size: 13.5px;">{proj.get('description', '')}</p>
            <ul class="highlights-list">{highlights}</ul>
        </div>"""

    mapping = {
        'NAME': data['basics']['name'],
        'LABEL': data['basics']['label'],
        'LINKS_GRID': links_html,
        'SUMMARY': data['basics']['summary'],
        'SKILLS_CONTAINER': skills_html,
        'EXPERIENCE_BLOCK': exp_html,
        'EDUCATION_TIMELINE_BLOCK': edu_html,
        'PROJECTS': project_html
    }
    
    rendered = Template(template_content).safe_substitute(mapping)
    os.makedirs('output', exist_ok=True)
    output_path = os.path.join('output', 'resume.html')
    with open(output_path, 'w', encoding='utf-8') as f: f.write(rendered)
    return output_path

class WorkspaceHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r', encoding='utf-8') as f: html = f.read()
            injected_html = html.replace('/* INITIAL_DATA_INJECTION */', f"const initialResumeData = {json.dumps(load_json_data())};")
            self.wfile.write(injected_html.encode('utf-8'))
        else: self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
        if self.path in ['/api/save', '/api/build']:
            with open('resume.json', 'w', encoding='utf-8') as f: json.dump(payload, f, indent=2, ensure_ascii=False)
            msg = "JSON updated."
            if self.path == '/api/build': build_resume_html(payload); msg = "Resume compiled to output/resume.html!"
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": msg}).encode('utf-8'))

if __name__ == '__main__':
    print(f"Dev server running at http://localhost:{PORT}")
    http.server.HTTPServer(('localhost', PORT), WorkspaceHandler).serve_forever()