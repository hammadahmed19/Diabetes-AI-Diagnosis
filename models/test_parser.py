import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import base64
import io

load_dotenv()

class TestReportParser:
    """Parse medical test reports using LLM vision capabilities"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"  # GPT-4 with vision
    
    def parse_test_report(self, image_file):
        """
        Extract medical test data from uploaded image/PDF
        Returns: dict with extracted values
        """
        try:
            # Get file extension
            filename = image_file.filename.lower()
            
            # Handle PDF files
            if filename.endswith('.pdf'):
                image_data = self._convert_pdf_to_image(image_file)
            else:
                # Handle image files
                image_data = image_file.read()
                # Ensure it's a supported format
                image_data = self._ensure_supported_format(image_data)
            
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Use GPT-4 Vision to extract data
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a medical data extraction specialist. 
                        Extract diabetes-related test values from lab reports.
                        Look for: glucose levels, HbA1c, BMI, weight, height, and patient age.
                        IMPORTANT: Extract age from patient info (e.g., "63Y/F" means 63 years old).
                        You must return ONLY valid JSON, no other text."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Extract the following information from this medical test report:
                                - Patient name (full name)
                                - Patient age (look for patterns like "63Y/F", "45 years", etc.)
                                - Glucose level (fasting or random) in mg/dL
                                - HbA1c percentage (if available)
                                - BMI (if available)
                                - Weight and Height (if available)
                                - Test date
                                - Any other diabetes-related markers
                                
                                IMPORTANT: 
                                - Extract age from formats like "63Y/F" (63 years old, Female)
                                - Look carefully at all visible text
                                - If glucose_type is not specified, try to infer from context
                                
                                Return ONLY this JSON format with no additional text:
                                {
                                    "patient_name": "full name" or null,
                                    "age": numeric_value or null,
                                    "glucose_level": numeric_value or null,
                                    "glucose_type": "fasting" or "random" or "postprandial" or null,
                                    "hba1c": numeric_value or null,
                                    "bmi": numeric_value or null,
                                    "weight": numeric_value or null,
                                    "height": numeric_value or null,
                                    "test_date": "date" or null,
                                    "other_findings": "text" or null
                                }"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            # Parse response
            import json
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON if there's extra text
            if not response_text.startswith('{'):
                # Find JSON in response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    response_text = response_text[json_start:json_end]
            
            result = json.loads(response_text)
            return {
                'success': True,
                'data': result,
                'message': 'Test report parsed successfully'
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {response_text if 'response_text' in locals() else 'No response'}")
            return {
                'success': False,
                'data': None,
                'message': 'Could not extract structured data from the report. Please try manual entry or a clearer image.'
            }
        except Exception as e:
            print(f"Test parsing error: {e}")
            return {
                'success': False,
                'data': None,
                'message': f'Error parsing test report: {str(e)}'
            }
    
    def _convert_pdf_to_image(self, pdf_file):
        """Convert all relevant PDF pages to images"""
        try:
            import fitz  # PyMuPDF
            
            # Read PDF
            pdf_bytes = pdf_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            images = []
            
            # Process all pages (up to 10 for performance)
            max_pages = min(len(pdf_document), 10)
            
            for page_num in range(max_pages):
                page = pdf_document[page_num]
                
                # Get page text to check relevance
                page_text = page.get_text().lower()
                
                # Check if page is diabetes-relevant
                diabetes_keywords = [
                    'glucose', 'sugar', 'diabetes', 'hba1c', 'hemoglobin a1c',
                    'fasting', 'random', 'blood sugar', 'glycated', 'a1c'
                ]
                
                is_relevant = any(keyword in page_text for keyword in diabetes_keywords)
                
                if is_relevant:
                    # Render page to image (higher resolution for better OCR)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
                    
                    # Convert to PIL Image
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    images.append(img)
            
            pdf_document.close()
            
            if not images:
                # If no relevant pages found, use first page
                pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                page = pdf_document[0]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
                pdf_document.close()
            
            # Combine multiple images vertically if needed
            if len(images) > 1:
                # Calculate total height
                total_height = sum(img.height for img in images)
                max_width = max(img.width for img in images)
                
                # Create combined image
                combined = Image.new('RGB', (max_width, total_height), 'white')
                
                y_offset = 0
                for img in images:
                    combined.paste(img, (0, y_offset))
                    y_offset += img.height
                
                final_img = combined
            else:
                final_img = images[0]
            
            # Convert to JPEG bytes
            img_byte_arr = io.BytesIO()
            final_img.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except ImportError:
            raise Exception("PDF support requires PyMuPDF. Install with: pip install pymupdf")
        except Exception as e:
            raise Exception(f"Error converting PDF: {str(e)}")
    
    def _ensure_supported_format(self, image_data):
        """Ensure image is in a supported format (PNG, JPEG, GIF, WEBP)"""
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Save as JPEG
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr.seek(0)
            
            return img_byte_arr.getvalue()
            
        except Exception as e:
            # If conversion fails, return original
            return image_data
    
    def validate_extracted_data(self, data):
        """Validate extracted medical data"""
        warnings = []
        
        if data.get('glucose_level'):
            glucose = float(data['glucose_level'])
            if glucose < 50 or glucose > 600:
                warnings.append('Glucose level seems unusual. Please verify.')
        
        if data.get('hba1c'):
            hba1c = float(data['hba1c'])
            if hba1c < 3 or hba1c > 20:
                warnings.append('HbA1c value seems unusual. Please verify.')
        
        if data.get('bmi'):
            bmi = float(data['bmi'])
            if bmi < 10 or bmi > 60:
                warnings.append('BMI seems unusual. Please verify.')
        
        return warnings
