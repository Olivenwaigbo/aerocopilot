from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.units import inch


# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# PDF STYLES
# ---------------------------------------------------------

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    spaceAfter=20,
)

HEADING_STYLE = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=14,
    spaceAfter=8,
)

BODY_STYLE = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontSize=10.5,
    leading=16,
    spaceAfter=8,
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def add_paragraph(story, text):
    story.append(Paragraph(text, BODY_STYLE))


def add_heading(story, text):
    story.append(Paragraph(text, HEADING_STYLE))


def create_pdf(filename, title, sections):
    """
    Creates a synthetic aviation technical document.
    """

    filepath = DOCUMENTS_DIR / filename

    document = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    story = []

    story.append(Paragraph(title, TITLE_STYLE))
    story.append(
        Paragraph(
            "AERO-100 Synthetic Aviation Documentation",
            BODY_STYLE,
        )
    )

    story.append(Spacer(1, 10))

    for section in sections:
        add_heading(story, section["heading"])

        for paragraph in section["content"]:
            add_paragraph(story, paragraph)

    document.build(story)

    print(f"Created: {filepath}")


# ---------------------------------------------------------
# DOCUMENT 1 — MAINTENANCE MANUAL
# ---------------------------------------------------------

maintenance_sections = [
    {
        "heading": "1.1 General Maintenance Principles",
        "content": [
            "Maintenance activities on the AERO-100 aircraft should be performed by appropriately trained personnel using the applicable approved maintenance documentation.",
            "Before maintenance begins, the aircraft should be placed in an appropriate maintenance condition and relevant systems should be isolated where required.",
            "Maintenance personnel should verify that required tools, equipment, replacement components, and documentation are available before beginning a maintenance task.",
        ],
    },
    {
        "heading": "2.1 Hydraulic System Maintenance",
        "content": [
            "The AERO-100 hydraulic system provides hydraulic power to selected aircraft systems and components.",
            "Routine hydraulic system maintenance includes inspection of hydraulic lines, fittings, reservoirs, connections, and associated components.",
            "Maintenance personnel should investigate visible hydraulic fluid leakage before returning the affected system to service.",
        ],
    },
    {
        "heading": "2.2 Hydraulic Fluid Leakage",
        "content": [
            "When hydraulic fluid leakage is identified, maintenance personnel should determine the approximate source of the leakage and inspect nearby fittings and hydraulic lines.",
            "Damaged or deteriorated hydraulic components should be assessed in accordance with the applicable maintenance procedure.",
            "Aircraft systems should not be returned to normal operation until the identified maintenance issue has been appropriately addressed.",
        ],
    },
    {
        "heading": "3.1 Engine Maintenance",
        "content": [
            "Engine maintenance activities should follow the applicable engine maintenance procedure.",
            "Maintenance personnel should inspect accessible engine components for visible damage, abnormal conditions, and signs of deterioration.",
            "Any abnormal finding should be documented and assessed using the appropriate maintenance process.",
        ],
    },
    {
        "heading": "4.1 Maintenance Documentation",
        "content": [
            "Maintenance activities and significant findings should be documented in accordance with the organization's approved maintenance recording process.",
            "Records should contain sufficient information to support traceability of maintenance actions and findings.",
        ],
    },
]


# ---------------------------------------------------------
# DOCUMENT 2 — OPERATIONS MANUAL
# ---------------------------------------------------------

operations_sections = [
    {
        "heading": "1.1 Aircraft Operating Philosophy",
        "content": [
            "The AERO-100 is a fictional narrow-body aircraft used in this research prototype.",
            "Flight crew should operate the aircraft using applicable operating procedures, checklists, and approved operational guidance.",
        ],
    },
    {
        "heading": "2.1 Pre-Flight Preparation",
        "content": [
            "Before flight, the flight crew should complete the applicable pre-flight preparation activities.",
            "Required aircraft documentation, operational information, weather information, and aircraft status should be reviewed before departure.",
        ],
    },
    {
        "heading": "2.2 Pre-Flight Aircraft Inspection",
        "content": [
            "The pre-flight aircraft inspection should include a visual assessment of relevant external aircraft areas and accessible components.",
            "Any abnormal condition identified during the inspection should be reported and evaluated before flight.",
        ],
    },
    {
        "heading": "3.1 Abnormal Operating Conditions",
        "content": [
            "When an abnormal aircraft condition occurs, flight crew should follow the applicable checklist and operational procedure.",
            "Crew members should communicate relevant information and maintain awareness of aircraft status throughout the event.",
        ],
    },
    {
        "heading": "4.1 Communication",
        "content": [
            "Effective communication between flight crew and relevant operational personnel supports safe and coordinated aircraft operations.",
            "Operational information should be communicated using established organizational procedures.",
        ],
    },
]


# ---------------------------------------------------------
# DOCUMENT 3 — SAFETY PROCEDURES
# ---------------------------------------------------------

safety_sections = [
    {
        "heading": "1.1 Safety Management",
        "content": [
            "Safety management activities are intended to identify hazards, assess risks, and support appropriate mitigation actions.",
            "Personnel should report relevant hazards and safety concerns through established organizational reporting channels.",
        ],
    },
    {
        "heading": "2.1 Hazard Identification",
        "content": [
            "Hazards may be identified through inspections, operational reports, maintenance findings, incident reports, or other safety information.",
            "Identified hazards should be documented sufficiently to support subsequent assessment.",
        ],
    },
    {
        "heading": "2.2 Risk Assessment",
        "content": [
            "Risk assessment should consider the potential severity and likelihood associated with an identified hazard.",
            "Risk assessments should be reviewed when new information becomes available or when operating conditions change.",
        ],
    },
    {
        "heading": "3.1 Maintenance Safety",
        "content": [
            "Maintenance personnel should follow applicable safety procedures before working on aircraft systems.",
            "Appropriate personal protective equipment should be used when required by the applicable task or organizational procedure.",
            "Energy sources and aircraft systems should be controlled or isolated when required to reduce maintenance hazards.",
        ],
    },
    {
        "heading": "4.1 Safety Reporting",
        "content": [
            "Personnel should report safety concerns, hazards, and relevant events through approved reporting channels.",
            "Safety reports should contain sufficient information to allow the organization to understand and investigate the reported concern.",
        ],
    },
]


# ---------------------------------------------------------
# DOCUMENT 4 — INSPECTION MANUAL
# ---------------------------------------------------------

inspection_sections = [
    {
        "heading": "1.1 Inspection Principles",
        "content": [
            "Aircraft inspections are performed to identify conditions that may require maintenance action or further assessment.",
            "Inspection activities should follow the applicable inspection procedure and use the required inspection equipment.",
        ],
    },
    {
        "heading": "2.1 Visual Inspection",
        "content": [
            "Visual inspection may include examination for visible damage, leakage, corrosion, loose components, deterioration, or other abnormal conditions.",
            "Inspection personnel should document relevant findings according to the applicable recording process.",
        ],
    },
    {
        "heading": "3.1 Hydraulic System Inspection",
        "content": [
            "The AERO-100 hydraulic system inspection should include examination of accessible hydraulic lines, fittings, connections, and associated components.",
            "Inspectors should check for visible hydraulic fluid leakage, damaged hydraulic lines, loose fittings, and signs of component deterioration.",
            "Where applicable, hydraulic pressure indications should be reviewed for abnormal conditions.",
            "Any significant abnormal finding should be documented and referred for appropriate maintenance assessment.",
        ],
    },
    {
        "heading": "3.2 Engine Inspection",
        "content": [
            "Engine inspection should include examination of accessible engine areas for visible damage, leakage, deterioration, and other abnormal conditions.",
            "Findings should be recorded and assessed using the applicable inspection process.",
        ],
    },
    {
        "heading": "4.1 Structural Inspection",
        "content": [
            "Structural inspection activities may include examination for visible cracks, deformation, corrosion, damage, or other conditions requiring further assessment.",
            "Inspection personnel should document relevant findings and escalate significant abnormalities according to applicable procedures.",
        ],
    },
]


# ---------------------------------------------------------
# CREATE DOCUMENTS
# ---------------------------------------------------------

if __name__ == "__main__":

    create_pdf(
        "aero100_maintenance_manual.pdf",
        "AERO-100 Maintenance Manual",
        maintenance_sections,
    )

    create_pdf(
        "aero100_operations_manual.pdf",
        "AERO-100 Operations Manual",
        operations_sections,
    )

    create_pdf(
        "aero100_safety_procedures.pdf",
        "AERO-100 Safety Procedures",
        safety_sections,
    )

    create_pdf(
        "aero100_inspection_manual.pdf",
        "AERO-100 Inspection Manual",
        inspection_sections,
    )

    print("\nAll synthetic AERO-100 documents created successfully.")