"""
PDF Report Generator Module
Creates professional medical reports
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import config

class ReportGenerator:
    """Generates PDF medical reports"""
    
    def __init__(self):
        """Initialize report generator"""
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Risk level styles
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#e74a3b'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskModerate',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#f6c23e'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#1cc88a'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
    
    def generate_report(self, filename, user_data, disease_type, prediction_result,
                       risk_probability, risk_level, input_parameters, recommendations):
        """
        Generate PDF report
        
        Args:
            filename: str - output PDF filename
            user_data: dict - user information
            disease_type: str - disease being tested
            prediction_result: int - 0 or 1
            risk_probability: float - probability (0-1)
            risk_level: str - 'Low', 'Moderate', 'High'
            input_parameters: dict - test parameters
            recommendations: list - health recommendations
        
        Returns:
            str - path to generated PDF
        """
        # Create PDF
        pdf_path = config.REPORTS_DIR / filename
        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
        
        # Container for elements
        elements = []
        
        # Header
        elements.append(self._create_header())
        elements.append(Spacer(1, 0.3 * inch))
        
        # Title
        disease_name = config.DISEASE_INFO[disease_type]['name']
        title = Paragraph(
            f"{disease_name} Risk Assessment Report",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report Info
        report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        report_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        info_data = [
            ['Report ID:', report_id],
            ['Report Date:', report_date],
            ['Patient:', user_data.get('full_name', user_data.get('username', 'N/A'))],
            ['Age:', str(user_data.get('age', 'N/A'))],
            ['Gender:', user_data.get('gender', 'N/A')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Separator line
        elements.append(self._create_line())
        elements.append(Spacer(1, 0.2 * inch))
        
        # Test Results Section
        results_title = Paragraph("Test Results", self.styles['CustomSubtitle'])
        elements.append(results_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Risk Assessment Box
        elements.append(self._create_risk_box(risk_level, risk_probability))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Prediction Result
        result_text = "Positive" if prediction_result == 1 else "Negative"
        result_color = colors.HexColor('#e74a3b') if prediction_result == 1 else colors.HexColor('#1cc88a')
        
        result_para = Paragraph(
            f"<b>Prediction:</b> <font color='{result_color}'>{result_text}</font>",
            self.styles['Normal']
        )
        elements.append(result_para)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Input Parameters Section
        params_title = Paragraph("Test Parameters", self.styles['CustomSubtitle'])
        elements.append(params_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        params_table = self._create_parameters_table(input_parameters)
        elements.append(params_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Recommendations Section
        rec_title = Paragraph("Health Recommendations", self.styles['CustomSubtitle'])
        elements.append(rec_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        for rec in recommendations:
            rec_para = Paragraph(f"• {rec}", self.styles['Normal'])
            elements.append(rec_para)
            elements.append(Spacer(1, 0.05 * inch))
        
        elements.append(Spacer(1, 0.3 * inch))
        
        # Doctor's Notes Section
        notes_title = Paragraph("Doctor's Notes", self.styles['CustomSubtitle'])
        elements.append(notes_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        notes_box = self._create_notes_box()
        elements.append(notes_box)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Disclaimer
        disclaimer = Paragraph(
            "<b>DISCLAIMER:</b> This report is generated by an AI system for educational purposes only. "
            "It should not be considered as a medical diagnosis. Please consult a qualified healthcare "
            "professional for proper medical advice and treatment.",
            self.styles['Normal']
        )
        elements.append(disclaimer)
        
        # Footer
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(self._create_line())
        elements.append(Spacer(1, 0.1 * inch))
        footer = Paragraph(
            f"Multi-Disease Risk Analytics System | Generated on {report_date}",
            ParagraphStyle(
                'footer',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return str(pdf_path)
    
    def _create_header(self):
        """Create report header"""
        header_data = [[
            Paragraph(
                "<b>🏥 Multi-Disease Risk Analytics</b>",
                ParagraphStyle(
                    'header',
                    parent=self.styles['Normal'],
                    fontSize=16,
                    textColor=colors.HexColor('#2c3e50'),
                    fontName='Helvetica-Bold'
                )
            )
        ]]
        
        header_table = Table(header_data, colWidths=[6.5*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        return header_table
    
    def _create_risk_box(self, risk_level, probability):
        """Create risk assessment box"""
        risk_style_map = {
            'Low': 'RiskLow',
            'Moderate': 'RiskModerate',
            'High': 'RiskHigh'
        }
        
        color_map = {
            'Low': colors.HexColor('#1cc88a'),
            'Moderate': colors.HexColor('#f6c23e'),
            'High': colors.HexColor('#e74a3b')
        }
        
        risk_data = [[
            Paragraph(f"Risk Level: {risk_level}", self.styles[risk_style_map[risk_level]]),
            Paragraph(f"{probability * 100:.1f}%", self.styles[risk_style_map[risk_level]])
        ]]
        
        risk_table = Table(risk_data, colWidths=[3.25*inch, 3.25*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color_map[risk_level].clone(alpha=0.1)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 2, color_map[risk_level]),
        ]))
        
        return risk_table
    
    def _create_parameters_table(self, parameters):
        """Create table for input parameters"""
        # Convert parameters to table data
        param_data = [['Parameter', 'Value']]
        
        for key, value in parameters.items():
            param_data.append([str(key), str(value)])
        
        param_table = Table(param_data, colWidths=[3*inch, 3*inch])
        param_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return param_table
    
    def _create_notes_box(self):
        """Create empty box for doctor's notes"""
        notes_data = [['']]
        notes_table = Table(notes_data, colWidths=[6.5*inch], rowHeights=[1.5*inch])
        notes_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ]))
        
        return notes_table
    
    def _create_line(self):
        """Create horizontal line"""
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch], rowHeights=[0.01*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.grey),
        ]))
        
        return line_table
