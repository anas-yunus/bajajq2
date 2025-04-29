from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import re

app = FastAPI()

@app.post("/get-lab-tests")
async def process_lab_report(file: UploadFile = File(...)):
    # Read image
    image = Image.open(io.BytesIO(await file.read()))

    # OCR
    ocr_text = pytesseract.image_to_string(image)

    # Log raw OCR output
    print("\n--- OCR EXTRACTED TEXT ---\n")
    print(ocr_text)

    # Parse the OCR result
    result = process_ocr_output(ocr_text)

    return JSONResponse(content=result)
def process_ocr_output(ocr_text):
    extracted_data = []

    # Split OCR text into lines
    lines = ocr_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Try to find a number (test value) inside the line
        match = re.search(r'(\d+\.?\d*)\s*([a-zA-Z/%]*)', line)
        if match:
            test_value = match.group(1)
            test_unit = match.group(2) if match.group(2) else "N/A"

            # The text before the number is likely the test name
            test_name = line[:match.start()].strip()

            # Only add if test_name is not empty
            if test_name:
                extracted_data.append({
                    "test_name": test_name,
                    "test_value": test_value,
                    "test_unit": test_unit,
                    "bio_reference_range": "N/A",
                    "lab_test_out_of_range": False
                })

    return {
        "is_success": True,
        "data": extracted_data
    }


# ✅ Working parser function
# def process_ocr_output(ocr_text):
#     extracted_data = []

#     # Simple pattern: Test name followed by number and optional unit
#     pattern = re.compile(r'([A-Za-z\s\-]+)(\d+\.?\d*)\s?([A-Za-z/]+)?')

#     matches = pattern.findall(ocr_text)

#     for match in matches:
#         test_name, test_value, test_unit = match

#         test_name = test_name.strip()
#         test_value = test_value.strip()
#         test_unit = test_unit.strip() if test_unit else "N/A"

#         extracted_data.append({
#             "test_name": test_name,
#             "test_value": test_value,
#             "test_unit": test_unit,
#             "bio_reference_range": "N/A",
#             "lab_test_out_of_range": False
#         })

#     return {
#         "is_success": True,
#         "data": extracted_data
#     }
