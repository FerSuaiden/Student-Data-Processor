from googleapiclient.discovery import build
from google.oauth2 import service_account
import math

def process_student_data(sheet, spreadsheet_id):
    # Get the total number of classes
    classes_data = sheet.values().get(spreadsheetId=spreadsheet_id, range="engenharia_de_software!A2:H2").execute()
    classes_value = classes_data.get("values", [])
    total_classes = int(classes_value[0][0].split(": ")[1])

    # Get the students data
    student_data_range = "engenharia_de_software!C4:F27"
    student_data = sheet.values().get(spreadsheetId=spreadsheet_id, range=student_data_range).execute()
    student_values = student_data.get("values", [])

    # Process each student's data
    processed_data = []
    for row in student_values:
        # Extract absences and calculate percentage
        absences = int(row[0])
        absences_percentage = (absences / total_classes) * 100

        # Determine the student's situation based on absences and average
        if absences_percentage > 25:
            situation = "Reprovado por Falta"
            final_exam_score = 0
        else:
            # Calculate the average of the three grades
            average = (float(row[1]) + float(row[2]) + float(row[3])) / 3

            if average < 50:
                situation = "Reprovado por Nota"
                final_exam_score = 0
            elif average < 70:
                situation = "Exame Final"
                # Calculate the final exam score needed
                final_exam_score = math.ceil(100 - average)
            else:
                situation = "Aprovado"
                final_exam_score = 0

        # Append the student's situation and final exam score to the processed data
        processed_data.append([situation, final_exam_score])

    # Update the spreadsheet with the processed data
    update_data = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range="engenharia_de_software!G4:H27",
        valueInputOption="USER_ENTERED",
        body={"values": processed_data}
    ).execute()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = "1KG5wQeOpDFrC-2vDh2gMFKh_pulMeukgVxN7XktKAdA"

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

process_student_data(sheet, SAMPLE_SPREADSHEET_ID)
