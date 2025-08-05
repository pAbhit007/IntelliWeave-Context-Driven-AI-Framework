#!/usr/bin/env python3
"""
Script to create a sample PDF for testing the RAG system
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_sample_pdf():
    # Create the documents directory if it doesn't exist
    os.makedirs('data/documents', exist_ok=True)
    
    # Create PDF
    doc = SimpleDocTemplate('data/documents/sample_document.pdf', pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
    )
    story.append(Paragraph("Sample Knowledge Base Document", title_style))
    story.append(Spacer(1, 12))
    
    # Content sections
    content = [
        ("About Artificial Intelligence", [
            "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can perform tasks that typically require human intelligence. These tasks include visual perception, speech recognition, decision-making, and language translation.",
            "",
            "Types of AI:",
            "1. Narrow AI: AI systems designed to perform specific tasks, such as image recognition or playing chess.",
            "2. General AI: Hypothetical AI that could understand, learn, and apply knowledge across various domains.", 
            "3. Superintelligence: AI that would surpass human intelligence in all domains."
        ]),
        ("Machine Learning", [
            "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It includes:",
            "",
            "• Supervised Learning: Learning with labeled examples",
            "• Unsupervised Learning: Finding patterns in data without labels",
            "• Reinforcement Learning: Learning through interaction with an environment"
        ]),
        ("Applications", [
            "AI is used in various applications including:",
            "• Healthcare diagnostics",
            "• Autonomous vehicles", 
            "• Natural language processing",
            "• Computer vision",
            "• Recommendation systems"
        ]),
        ("Technology Trends", [
            "Cloud Computing: Cloud computing has revolutionized how businesses store and process data, offering scalability and cost-effectiveness.",
            "",
            "Internet of Things (IoT): IoT connects everyday devices to the internet, enabling smart homes, cities, and industrial applications.",
            "",
            "Blockchain Technology: Blockchain provides a decentralized and secure way to record transactions and store data."
        ])
    ]
    
    for section_title, paragraphs in content:
        # Section header
        story.append(Paragraph(section_title, styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Section content
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para, styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print("Sample PDF created successfully at data/documents/sample_document.pdf")

if __name__ == "__main__":
    create_sample_pdf()