import json
import re
from google.cloud import vision
from google.cloud import storage
import os
import time

# Replace 'Google credentials json file' with file downloaded from Google Cloud Console
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="[[Google credentials json file]]"

#'list.txt' = list of files in Google Cloud bucket
items = [line.rstrip('\n') for line in open('list.txt')]

def async_detect_document(gcs_source_uri):
    """OCR with PDF/TIFF as source files on GCS"""

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 50

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)

    split = os.path.split(gcs_source_uri)[1]
    split2 = os.path.splitext(split)[0]

    gcs_destination_uri = "[[output storage bucket]]" + split2 + "_"
    print(gcs_destination_uri)

    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)

    # The actual response for the first page of the input file.
    first_page_response = response['responses'][0]
    annotation = first_page_response['fullTextAnnotation']

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print('Full text:\n')
    print(annotation['text'])

def write_to_text(gcs_input_uri, gcs_destination_uri):

    storage_client = storage.Client()
    match2 = re.match(r'gs://([^/]+)/(.+)', gcs_input_uri)
    bucket_name2 = match2.group(1)
    prefix2 = match2.group(2)

    bucket2 = storage_client.get_bucket(bucket_name2)

    # List objects with the given prefix.
    blob_list2 = list(bucket2.list_blobs(prefix=prefix2))
    print('Output files:')
    for blob in blob_list2:
        print(blob.name)

def process_pdfs():
    for item in items:
        gcs_source_uri = str(item)

        async_detect_document(gcs_source_uri)
        time.sleep(1)

process_pdfs()
