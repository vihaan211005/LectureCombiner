import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader

def convert_pptx_to_pdf(pptx_path, output_dir):
    pdf_path = output_dir / (pptx_path.stem + ".pdf")
    if pdf_path.exists():
        print(f"✅ Already converted: {pdf_path.name}")
        return pdf_path

    print(f"🔄 Converting to PDF: {pptx_path.name}")
    try:
        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(pptx_path)
        ], check=True)
        return pdf_path if pdf_path.exists() else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed for {pptx_path.name}: {e}")
        return None

def download_and_merge(json_path, download_dir, combined_pdf_name="combined.pdf"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "data" not in data or not isinstance(data["data"], list):
        print("❌ Invalid JSON structure: Expected 'data' key with a list of lectures.")
        sys.exit(1)

    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    merger = PdfMerger()
    current_page = 0

    for lecture in data["data"]:
        title = lecture.get("title", "Untitled")
        for file in lecture.get("files", []):
            file_id = file["id"]
            original_filename = file["filename"]
            ext = Path(original_filename).suffix.lower()
            filename = f"{file_id}_{original_filename}"
            filepath = download_path / filename
            url = file["fileUrl"]

            print(f"➡️ Checking: {filename} (ID: {file_id})")

            if not filepath.exists():
                print(f"⬇️  Downloading: {filename}")
                try:
                    r = requests.get(url)
                    r.raise_for_status()
                    with open(filepath, "wb") as out:
                        out.write(r.content)
                except Exception as e:
                    print(f"❌ Failed to download {filename}: {e}")
                    continue
            else:
                print(f"✅ Already exists: {filename}")

            # Handle pptx conversion
            if file["filemime"] == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                pdf_path = convert_pptx_to_pdf(filepath, download_path)
                if not pdf_path or not pdf_path.exists():
                    continue
            elif file["filemime"] == "application/pdf":
                pdf_path = filepath
            else:
                print(f"⏭️  Unsupported file type: {file['filemime']}")
                continue

            try:
                reader = PdfReader(str(pdf_path))
                num_pages = len(reader.pages)
                merger.append(reader)
                merger.add_outline_item(title, page_number=current_page)
                print(f"🔖 Added bookmark: '{title}' at page {current_page}")
                current_page += num_pages
            except Exception as e:
                print(f"❌ Failed to process {pdf_path.name}: {e}")

    combined_path = download_path / combined_pdf_name
    merger.write(str(combined_path))
    merger.close()
    print(f"\n📘 Combined PDF created at: {combined_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python organizer.py <path_to_json> <download_dir> [combined_pdf_name]")
        sys.exit(1)

    json_file = sys.argv[1]
    download_directory = sys.argv[2]
    output_name = sys.argv[3] if len(sys.argv) > 3 else "combined.pdf"

    download_and_merge(json_file, download_directory, output_name)
