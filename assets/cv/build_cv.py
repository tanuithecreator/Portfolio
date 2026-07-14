"""Build Julian Tanui's CV (.docx). Formatting mirrors the existing PDF style:
- Centered ALL-CAPS name
- Centered single-line contact + Portfolio link
- Section headings: ALL CAPS, blue, underlined
- Bullets with bold lead labels
- Times New Roman serif body
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HEADING_COLOR = RGBColor(0x1F, 0x3A, 0x6B)
LINK_COLOR = RGBColor(0x05, 0x63, 0xC1)
BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(11)


def set_run(run, *, bold=False, italic=False, size=BODY_SIZE, color=None,
            font=BODY_FONT, underline=False):
    run.font.name = font
    run.font.size = size
    run.bold = bold
    run.italic = italic
    run.underline = underline
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), font)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    set_run(run, bold=True, size=Pt(12), color=HEADING_COLOR, underline=True)
    return p


def add_bullet(doc, segments):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    for text, opts in segments:
        run = p.add_run(text)
        set_run(run, bold=opts.get("bold", False), italic=opts.get("italic", False))
    return p


def add_body(doc, text, *, align=None, bold=False, italic=False, space_after=Pt(4)):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = space_after
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    set_run(run, bold=bold, italic=italic)
    return p


def build():
    doc = Document()

    style = doc.styles["Normal"]
    style.font.name = BODY_FONT
    style.font.size = BODY_SIZE
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), BODY_FONT)

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("JULIAN TANUI")
    set_run(run, bold=True, size=Pt(22))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("Nairobi, KE | +254 717302004 | julian.tanui01@gmail.com")
    set_run(run)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("Portfolio")
    set_run(run, color=LINK_COLOR, underline=True)

    # Professional Summary
    add_section_heading(doc, "PROFESSIONAL SUMMARY")
    add_body(
        doc,
        "Software and AI Engineer with a BSc in Informatics and Computer Science, "
        "currently building production software for the climate technology sector "
        "at Verst Carbon. My work spans full-stack web applications, AI agent "
        "systems, and data pipelines, from a financial risk engine for carbon-credit "
        "portfolios to a real-time meeting intelligence platform and a deepfake "
        "detection system. Recognized for academic excellence through the Dean's "
        "List and experienced in international innovation challenges, I focus on "
        "turning complex problems into reliable, well-crafted products.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )

    # Technical Skills
    add_section_heading(doc, "TECHNICAL SKILLS")
    skills = [
        ("Languages", "Python, TypeScript, JavaScript, Kotlin, SQL."),
        ("Frameworks", "Next.js, React, FastAPI, Flask, Node.js/Express, PyTorch, TensorFlow."),
        ("AI & Agents", "LLM agents (LangGraph, LangChain, multi-agent orchestration), model-selection routing across Claude/GPT-4o/Gemini, prompt engineering & evaluation frameworks."),
        ("Retrieval & ML", "RAG (FAISS, BM25, pgvector, ontology-backed retrieval), vector stores & semantic search, Computer Vision (CNNs, ResNet50), NLP."),
        ("Data Engineering", "ETL/ELT pipelines, data-quality/validation & freshness monitoring, geospatial sources (NASA FIRMS, GFW, GDELT, OpenStreetMap), interactive map dashboards."),
        ("Cloud & DevOps", "Docker, CI/CD, PostgreSQL/Supabase, Redis, MinIO, Modal, Inngest, Railway, Cloudflare Pages."),
        ("Tools", "Git/GitHub, Linux Systems, Cisco Networking, IoT Sensors."),
    ]
    for label, desc in skills:
        add_bullet(doc, [(label, {"bold": True}), (f": {desc}", {})])

    # Education
    add_section_heading(doc, "EDUCATION")
    add_body(
        doc,
        "Strathmore University, Nairobi | Bachelor of Informatics and Computer Science",
        bold=True,
        space_after=Pt(2),
    )
    add_body(
        doc,
        "Coursework completed, December 2025 | Degree conferment: August 2026",
        italic=True,
        space_after=Pt(2),
    )
    add_bullet(doc, [
        ("Honors", {"bold": True}),
        (": Dean's List Award (2024-2025, 2025-2026) – Recognized for outstanding academic performance.", {}),
    ])
    add_bullet(doc, [
        ("Leadership", {"bold": True}),
        (": Local Committee Vice President for Finance and Legalities; Project Manager – SDG Hub, Strathmore.", {}),
    ])
    add_bullet(doc, [
        ("Relevant Coursework", {"bold": True}),
        (": Data Structures and Algorithms, Software Engineering, Machine Learning, Advanced Database Systems, Advanced Networking, Project Management.", {}),
    ])

    # Professional Experience
    add_section_heading(doc, "PROFESSIONAL EXPERIENCE")

    add_body(
        doc,
        "Verst Carbon | SWE/AI Engineering Intern | Feb 2026 – Present",
        bold=True,
        space_after=Pt(2),
    )
    for b in [
        "Designed and built multi-agent AI systems (LangGraph, LangChain) that automate multi-step analysis across geospatial, infrastructure, economic, and monitoring data, routing each task to the most suitable language model for accuracy and cost efficiency.",
        "Applied retrieval-augmented generation to ground AI responses in trusted sources, keeping outputs accurate and traceable.",
        "Built full-stack web applications with Next.js, React, and Python (FastAPI, Node.js), including authenticated dashboards, interactive maps, and real-time chat.",
        "Developed data pipelines that ingest and validate large geospatial and economic datasets, with automated quality and freshness checks.",
        "Containerized and deployed services with Docker and CI/CD, adding monitoring and evaluation to track reliability.",
    ]:
        add_bullet(doc, [(b, {})])

    add_body(
        doc,
        "CIC Insurance Group | ICT Intern | Jan 2025 – April 2025",
        bold=True,
        space_after=Pt(2),
    )
    for b in [
        "Provided enterprise-level technical support, resolving complex ticket escalations and ensuring operational continuity.",
        "Managed network infrastructure, troubleshooting outages and optimizing performance for domain connectivity.",
        "Configured hardware assets (laptops, mobile devices), ensuring strict adherence to security protocols.",
    ]:
        add_bullet(doc, [(b, {})])

    add_body(
        doc,
        "Kenya National Library Service (KNLS) | Volunteer & Trainer | Jan 2024 – Mar 2024",
        bold=True,
        space_after=Pt(2),
    )
    for b in [
        "Led digital literacy workshops, teaching computer proficiency to students and community members.",
        "Assisted in organizing educational workshops and fostering a collaborative learning environment.",
        "Assisted in front desk services and library resource organization.",
    ]:
        add_bullet(doc, [(b, {})])

    # Hackathons
    add_section_heading(doc, "HACKATHONS & INNOVATION CHALLENGES")
    add_bullet(doc, [
        ("International Energy & Sustainability Hackathon (2026)", {"bold": True}),
        (": Completed the 2026 cohort, developing sustainable energy solutions.", {}),
    ])
    add_bullet(doc, [
        ("Inflection AI Hackathon (Climate Change)", {"bold": True}),
        (": Developed 'EcoCoin,' a fintech solution for trading carbon credits for real currency to incentivize climate action.", {}),
    ])
    add_bullet(doc, [
        ("Oracle Hackathon (Climate Change)", {"bold": True}),
        (": Built 'Smart IoT Farm,' an integrated system using sensors and AI to monitor soil health and automate irrigation.", {}),
    ])

    # Selected Engineering Projects
    add_section_heading(doc, "SELECTED ENGINEERING PROJECTS")

    add_body(doc, "AI & Machine Learning", bold=True, space_after=Pt(2))
    add_bullet(doc, [
        ("Meeting Intelligence Engine (AI + Real-time Systems)", {"bold": True}),
        (": An end-to-end platform that captures meetings, produces live transcripts with speaker labels, and generates AI summaries, action items, and searchable chat. Includes calendar integration, secure access controls, and auto-generated weekly audio recaps. Built with GPT-4o on a React and Python stack.", {}),
    ])
    add_bullet(doc, [
        ("DeepDetect (AI/ML)", {"bold": True}),
        (": An explainable deep-learning system for detecting deepfake images and video, trained on a large public dataset with strong accuracy. Provides visual explanations of its predictions, video analysis, and admin reporting. Built with a ResNet50 model, React/TypeScript, and Flask.", {}),
    ])
    add_bullet(doc, [
        ("Project Rainmaker (AI Sales Agent)", {"bold": True}),
        (": An AI sales agent (LangGraph) that researches businesses online, evaluates their websites for marketing gaps, scores leads, and generates outreach reports. Developed for Okara AI's automated marketing platform.", {}),
    ])
    add_bullet(doc, [
        ("Gaming RAG Assistant (AI)", {"bold": True}),
        (": A question-answering assistant over game documentation that combines semantic and keyword search for accurate, character-styled responses. Built with HuggingFace models and deployed on Streamlit Cloud.", {}),
    ])

    add_body(doc, "Climate & Fintech", bold=True, space_after=Pt(2))
    add_bullet(doc, [
        ("OfftakeOS (Fintech + AI Automation)", {"bold": True}),
        (": An automated financial risk engine for carbon-credit portfolios that ingests forward contracts, monitors real-world environmental and market data, and scores delivery risk on interactive dashboards. Built with Next.js, Flask, and PostgreSQL, backed by a comprehensive automated test suite.", {}),
    ])
    add_bullet(doc, [
        ("CarbonVerify (Fullstack + DevOps)", {"bold": True}),
        (": A carbon-credit auditing dashboard with project mapping, sensor-data verification, and a certificate-issuing workflow. Built with React, a Node.js/Express API, PostgreSQL, and a full CI/CD pipeline.", {}),
    ])

    add_body(doc, "Mobile & Web", bold=True, space_after=Pt(2))
    add_bullet(doc, [
        ("CasaControl (Mobile)", {"bold": True}),
        (": A smart-home management mobile app built with Kotlin, enabling remote appliance control.", {}),
    ])
    add_bullet(doc, [
        ("CommunityPlus (Web)", {"bold": True}),
        (": Web-based donation platform bridging donors and receivers to facilitate community support.", {}),
    ])

    # Achievements & Certifications
    add_section_heading(doc, "ACHIEVEMENTS & CERTIFICATIONS")
    add_bullet(doc, [
        ("Dean's List Award (2024-2025, 2025-2026)", {"bold": True}),
        (": Awarded for maintaining a high GPA and demonstrating academic leadership.", {}),
    ])
    add_bullet(doc, [
        ("NSK AI RAG Bootcamp", {"bold": True}),
        (": Completed intensive training on building Retrieval-Augmented Generation systems.", {}),
    ])
    add_bullet(doc, [
        ("Cisco Certified", {"bold": True}),
        (": IT Essentials (Cisco Networking Academy) – proficient in hardware assembly, maintenance, and security.", {}),
    ])
    add_bullet(doc, [
        ("Cisco Certified", {"bold": True}),
        (": Computer Networks (Cisco Networking Academy).", {}),
    ])

    # Leadership & Activities
    add_section_heading(doc, "LEADERSHIP & ACTIVITIES")
    add_bullet(doc, [
        ("Local Committee Vice President", {"bold": True}),
        (" – Finance & Legalities, Strathmore University.", {}),
    ])
    add_bullet(doc, [
        ("Project Manager", {"bold": True}),
        (" – SDG Hub, Strathmore University.", {}),
    ])
    add_bullet(doc, [
        ("Member", {"bold": True}),
        (": Google Student Developer Club (GDSC), Strathmore University.", {}),
    ])
    add_bullet(doc, [
        ("Member", {"bold": True}),
        (": Strathmore Computing and Engineering Sciences Association.", {}),
    ])
    add_bullet(doc, [
        ("Registered Member", {"bold": True}),
        (": The Kenya Red Cross Society.", {}),
    ])

    out = r"C:\Users\USER\AD_DEV\Portfolio\assets\cv\Julian Tanui CV.docx"
    doc.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    build()
