import spacy
import sys
from pathlib import Path

# Find the absolute path to the 'en_core_web_sm' model relative to the script's directory
def get_model_path():
    # Locate the base 'ResumeAnalyse' folder, wherever the user places it

    model_path = Path("ResumeAnalyzer") / "Project" / "venv" / "Lib" / "site-packages" / "en_core_web_sm" / "en_core_web_sm-3.8.0"
    return str(model_path)

# Load the model using the dynamic path
try:
    model_path = get_model_path()
    nlp = spacy.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)




job_role_keywords = {
    "Data Analyst": ["excel", "microsoft excel", "r programming", "mysql", "tableau", "power bi", "sas", "data mining", "data visualization", "statistical analysis"],
    "Web Developer": [".net", "html", "css", "javascript", "php", "react", "angular", "vue", "bootstrap", "responsive design", "api integration"],
    "Software Developer": ["java", "python", "c++", "c#", "git", "spring boot", "django", "flask", "tdd", "agile methodologies", "restful services"],
    "Software Engineer": ["java", "python", "c++", "c#", "design patterns", "algorithms", "data structures", "git", "debugging", "unit testing", "microservices"],
    "Cybersecurity Specialist": ["network security", "snort", "wireshark", "kali linux", "penetration testing", "threat detection", "nmap", "incident response", "forensics"],
    "Cloud Engineer": ["aws", "azure", "docker", "kubernetes", "terraform", "cloudformation", "serverless", "cloud security", "serverless architecture"],
    "IT Helpdesk Technician": ["ticketing system", "active directory", "windows server", "troubleshooting", "vpn", "dns", "remote desktop", "sccm", "customer service", "network troubleshooting"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "data modeling", "mlops", "scikit-learn", "nlp", "deep learning", "model evaluation", "data preprocessing"],
    "Blockchain Engineer": ["solidity", "cryptography", "ethereum", "smart contracts", "web3", "hyperledger", "dapps", "decentralized applications", "smart contract auditing"],
    "DevOps Engineer": ["ci/cd", "jenkins", "docker", "ansible", "terraform", "kubernetes", "bash scripting", "gitlab", "monitoring tools", "release management"],
    "Database Administrator": ["mysql", "postgresql", "mongodb", "oracle", "backup", "replication", "performance tuning", "database security", "data modeling"],
    "AI Specialist": ["nlp", "deep learning", "chatbot", "bert", "transformer", "computer vision", "openai", "llms", "reinforcement learning", "automated reasoning"],
    "Data Scientist": ["python", "big data", "hadoop", "spark", "statistical analysis", "data visualization", "jupyter", "feature engineering", "data cleaning"],
    "Network Engineer": ["cisco", "firewall", "vpn", "mpls", "switching", "routing protocols", "ccna", "ospf", "bgp", "network design", "wireless technologies"],
    "UI/UX Designer": ["figma", "adobe xd", "wireframing", "prototyping", "user experience", "a/b testing", "design systems", "user research", "interaction design"],
    "Cloud Architect": ["aws", "azure", "gcp", "microservices", "cloud infrastructure", "architecture design", "cloud migration", "disaster recovery planning"],
    "IT Project Manager": ["agile", "scrum", "project planning", "jira", "risk management", "pmp", "ms project", "stakeholder communication", "project risk assessment"],
    "Systems Administrator": ["windows server", "linux", "vmware", "bash", "active directory", "automation", "sccm", "network configuration", "security updates"],
    "Technical Support Engineer": ["troubleshooting", "itil", "customer support", "hardware", "remote desktop", "helpdesk", "system configuration", "customer relationship management"],
    "Information Security Analyst": ["soc", "siem", "incident response", "threat intelligence", "vulnerability scanning", "risk assessment", "penetration testing", "security auditing"],
    "Mobile App Developer": ["swift", "kotlin", "react native", "flutter", "android studio", "ios", "mobile ux", "cross-platform development", "app monetization"],
    "Game Developer": ["unity", "unreal engine", "c#", "game physics", "3d modeling", "shader programming", "user interface design", "storytelling in games"],
    "Business Analyst": ["requirement gathering", "process modeling", "business process management", "confluence", "uml", "user stories", "data analysis", "stakeholder management"],
    "IT Consultant": ["digital transformation", "enterprise architecture", "strategy consulting", "sap", "oracle", "process improvement", "business process optimization", "technology strategy"],
    "IT Auditor": ["compliance", "sox", "pci dss", "risk management", "audit logs", "iso 27001", "internal controls", "audit frameworks", "regulatory compliance"],
    "Network Administrator": ["lan", "wan", "dns", "dhcp", "firewall", "vpn", "switches", "routers", "load balancing", "network monitoring tools", "wireless networking"],
    "Penetration Tester": ["burp suite", "nmap", "metasploit", "owasp", "ethical hacking", "exploitation frameworks", "security assessments", "risk management"],
    "ERP Consultant": ["sap", "oracle erp", "crm", "workday", "data migration", "integration", "erp implementation", "business process integration", "customization"],
    "Site Reliability Engineer (SRE)": ["observability", "monitoring", "grafana", "prometheus", "alerting", "chaos engineering", "incident management", "site reliability practices"],
    "IT Executive": ["strategic planning", "vendor management", "it governance", "budgeting", "stakeholder management", "kpi", "strategic initiatives", "technology governance"],
    "IT Manager": ["team leadership", "agile", "vendor management", "resource planning", "sla", "budget management", "team development", "performance management"],
    "IT Business Analyst": ["process analysis", "bpmn", "requirements documentation", "stakeholder analysis", "gap analysis", "business case development", "change management"],
    "Network Security Engineer": ["firewalls", "vpn", "ids", "ips", "encryption", "cyber defense", "incident response planning", "network protocols"],
    "Software Architect": ["design patterns", "microservices", "system design", "soa", "uml", "scalability", "architecture", "architecture frameworks", "design thinking"],
    "Full Stack Developer": ["javascript", "node.js", "react", "mongodb", "express", "api", "backend", "frontend", "devops practices", "agile development"],
    "Business Intelligence Analyst": ["data visualization", "sql", "data warehousing", "power bi", "tableau", "business metrics", "data storytelling"],
    "Data Engineer": ["python", "sql", "hadoop", "spark", "data pipeline", "etl", "cloud data warehousing", "data lakes"],
    "Augmented Reality (AR) Developer": ["augmented reality", "unity", "c#", "ar kit", "vuforia", "3d modeling", "computer vision"],
    "Virtual Reality (VR) Developer": ["virtual reality", "unreal engine", "3d graphics", "c++", "game design", "immersive experiences"],
    "IoT Developer": ["iot protocols", "mqtt", "hardware programming", "embedded systems", "cloud integration", "data analytics", "edge computing"],
    "Robotics Engineer": ["robotics", "programming", "mechanical design", "control systems", "sensors", "automation", "c++", "python"],
    "Natural Language Processing (NLP) Engineer": ["nlp", "python", "tensorflow", "language models", "text analysis", "sentiment analysis", "chatbot development"],
    "Research Scientist": ["data analysis", "statistical modeling", "experimentation", "literature review", "report writing", "research methodologies"],
    "Game Designer": ["level design", "game mechanics", "storyboarding", "playtesting", "narrative design", "game development tools"],
    "Quality Assurance (QA) Engineer": ["test automation", "manual testing", "selenium", "qa methodologies", "bug tracking", "api testing", "performance testing"],
    "Mobile Game Developer": ["unity", "c#", "ios", "android", "game mechanics", "mobile optimization", "monetization strategies"],
    "Cryptography Engineer": ["encryption algorithms", "security protocols", "ssl/tls", "data integrity", "public key infrastructure (PKI)", "secure communications"],
    "Supply Chain Analyst": ["data analysis", "supply chain management", "logistics", "inventory management", "forecasting", "erp systems"],
    "Technical Writer": ["technical documentation", "user manuals", "api documentation", "content management", "visual communication", "writing standards"],
    "SEO Specialist": ["keyword research", "on-page SEO", "off-page SEO", "analytics", "google search console", "content strategy", "link building"],
    "Digital Marketing Specialist": ["social media marketing", "content marketing", "email marketing", "google analytics", "seo", "campaign management"],
    "Data Privacy Officer": ["data protection", "gdpr compliance", "risk management", "data governance", "privacy policies", "regulatory requirements"],
    "IT Operations Manager": ["it operations", "service delivery", "incident management", "change management", "process improvement", "stakeholder communication"],
    "Research and Development (R&D) Engineer": ["research methodologies", "product development", "technical documentation", "prototyping", "market research", "innovation"],
    "Salesforce Developer": ["salesforce", "apex", "visualforce", "lightning components", "crm", "data migration", "api integration", "customization"],
    "Mobile UI/UX Designer": ["mobile design", "responsive design", "user research", "wireframing", "prototyping", "user testing", "accessibility"],
    "Penetration Tester": ["ethical hacking", "vulnerability assessment", "network scanning", "web application security", "risk management", "incident response"],
    "Technical SEO Specialist": ["technical audits", "website optimization", "xml sitemaps", "schema markup", "page speed", "mobile optimization"],
    "Digital Marketing Specialist": ["social media marketing", "content marketing", "email marketing", "google analytics", "seo", "campaign management"],
    "Data Privacy Officer": ["data protection", "gdpr", "compliance", "risk assessment", "policy development", "data governance"],
}







def analyze_resume(resume_text):

    doc = nlp(resume_text.lower())
    recommendations = []


    extracted_skills = set(token.text for token in doc if token.is_alpha and not token.is_stop)


    for role, keywords in job_role_keywords.items():

        matched_skills = [skill for skill in keywords if skill in extracted_skills]
        skill_count = len(matched_skills)

        # Add jobs based on matched skills
        if skill_count >= 4:
            recommendations.append((role, skill_count, "Highly recommended"))
        elif skill_count == 3:
            recommendations.append((role, skill_count, "Recommended"))
        elif skill_count == 2:
            recommendations.append((role, skill_count, "Suggested"))


    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations

if __name__ == "__main__":
    try:

        resume_text = sys.stdin.read().strip()
        if not resume_text:
            raise ValueError("No input text provided.")


        resume_text = resume_text.encode('utf-8', 'replace').decode('utf-8')


        results = analyze_resume(resume_text)

        print("\n".join([f"{role} (matched skills: {count}, {status})" for role, count, status in results]))

    except Exception as e:

        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)