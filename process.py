import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import re
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import zipfile


def process_excel_file(file_path):
    # Load the Excel file into a pandas DataFrame
    pokemon_db = pd.read_excel(file_path)

    # Define the paths to the directories containing the images
    backgrounds_path = "/path/to/backgrounds"
    rings_path = "/path/to/rings"
    pokemons_path = "/path/to/pokemon_resized"
    banners_path = "/path/to/banners"
    symbols_path = "/path/to/symbols"
    attack_strength_path = "/path/to/attack_strengths"
    evolution_path = "/path/to/evolution"

    # Your existing processing logic here

    # Zip the artifacts
    zip_filename = "artifacts.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for root, dirs, files in os.walk("/path/to/artifacts"):
            for file in files:
                zipf.write(os.path.join(root, file))

    # Upload to Google Drive
    upload_to_google_drive(zip_filename)


def upload_to_google_drive(file_path):
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    SERVICE_ACCOUNT_FILE = "path/to/service_account.json"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=credentials)

    file_metadata = {"name": os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype="application/zip")
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print("File ID: %s" % file.get("id"))
