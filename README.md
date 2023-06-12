# huxtable-ocr

These scripts were used to run OCR on a corpus of ~1,500 articles by the architectural critic Ada Louise Huxtable.

## Getting Started

This code utilizes the Google Vision API and Google Cloud storage.

## Usage

1. **google_pdf_ocr.py**
Run OCR on PDF files stored in the cloud. Writes JSON output to the cloud.

2. Download output using Google Cloud CLI in terminal
       ./google-cloud-sdk/bin/gcloud init
       gsutil cp -r [GOOGLE FOLDER] [OUTPUT FOLDER]
       
3. **json_to_csv_rename.py**
Write all output (filename, detected text) to a single CSV.

## Acknowledgments

Code from [Google Cloud Vision API](https://cloud.google.com/vision/docs/samples/vision-async-batch-annotate-images).


