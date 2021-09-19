from __future__ import print_function
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from log_handler import *


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1K5BovXNzvfPh-7pB0ROizHN5aXfb_Fbq7N5r3Ojht-w"
SAMPLE_RANGE_NAME = "A:A"


class Brands:
    def __init__(self) -> None:
        self.uhren = []
        logger.info(f"getting brands from google sheets...")
        self.initialize()
        logger.info(f"retrieved {len(self.uhren)} brands from google sheets")

    def initialize(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """

        creds = service_account.Credentials.from_service_account_file(
            "credentials.json", scopes=SCOPES
        )

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )

        values = result.get("values", [])

        self.uhren = list(map(lambda x: x[0], values))
