#!/usr/bin/env python
# coding: utf-8

# In[80]:


from pdf2image import convert_from_path
import cv2
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def process_pdf(input_pdf, output_pdf, operation='erosion', kernel_size=1):
    images = convert_from_path(input_pdf)
    processed_images = []

    # Define A4 size and the kernel for erosion or dilation
    a4_width, a4_height = A4  # ReportLab uses points, 1 point = 1/72 inch
    pixels_per_point = 1  # Adjust this based on your required DPI, e.g., 300 DPI = 300/72
    a4_width_pixels = int(a4_width * pixels_per_point)
    a4_height_pixels = int(a4_height * pixels_per_point)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    for image in images:
        # Convert PIL Image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply erosion or dilation
        if operation == 'erosion':
            processed_image = cv2.erode(open_cv_image, kernel, iterations=1)
        else:  # dilation
            processed_image = cv2.dilate(open_cv_image, kernel, iterations=1)
        
        # Resize image to fit A4
        processed_image_resized = cv2.resize(processed_image, (a4_width_pixels, a4_height_pixels), interpolation=cv2.INTER_AREA)
        
        # Convert back to PIL Image and add to list
        processed_images.append(Image.fromarray(cv2.cvtColor(processed_image_resized, cv2.COLOR_BGR2RGB)))

    # Create a new PDF with processed and resized images
    c = canvas.Canvas(output_pdf, pagesize=A4)
    for img in processed_images:
        img_path = "temp_image.jpg"
        img.save(img_path)
        c.drawImage(img_path, 0, 0, width=a4_width, height=a4_height)
        c.showPage()
    c.save()

# Specify your input and output PDF file paths
input_pdf_path = r"C:\Users\Acer\Desktop\test_pdf\testing.pdf"
output_pdf_path = r"C:\Users\Acer\Desktop\out_pdf\testing_ero.pdf"
process_pdf(input_pdf_path, output_pdf_path, operation='erosion', kernel_size=1)


# In[ ]:




