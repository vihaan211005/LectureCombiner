# LectureCombiner

**LectureCombiner** is a simple Python utility that automates the process of downloading lecture files (PDFs or PPTX) from a JSON file provided by your college portal, converts them to PDFs if needed, and merges them into one neat, bookmarked PDF for easy access and sharing.

---

## Features

- Automatically downloads lecture materials
- Converts PPTX files to PDF using LibreOffice
- Merges all PDFs into a single file with bookmarks for each lecture
- Easy to run with just one command
- Saves time for students who want a consolidated course PDF

---

## Requirements

- Python 3.7+
- [LibreOffice](https://www.libreoffice.org/download/download/) (for PPTX to PDF conversion)
- Python packages:  
  ```bash
  pip install requests PyPDF2
  ```

---

## How to Get the JSON File from Hello IITK

To use this tool, you need a `.json` file containing lecture metadata. Here's how to get it:

1. **Go to** [hello.iitk.ac.in](https://hello.iitk.ac.in) and log in using your IITK credentials.
2. Navigate to the **Lectures** tab in your course (see sidebar on the left).
3. **Open Developer Tools**:
   - Press `F12` or right-click anywhere on the page and select **Inspect**.
   - Go to the **Network** tab.
4. **Reload the page** (press `F5`) with the Network tab open.
5. Filter requests by **XHR** or **Fetch**.
6. Look for a request with a name like `lectures` in the URL (refer to the screenshot).
7. Click the request and switch to the **Response** tab.
8. **Right-click** the JSON response and click **Save as...** or copy the content and paste into a new file named `lec.json`.

---

## Run script
  ```bash
  python organizer.py <path_to_json> <download_dir> [combined_pdf_name]
  ```
