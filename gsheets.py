import os.path,gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re
import csv

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'xxxx'
RANGE_NAME = 'prices!A1:E'

def main():
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json",SCOPES)
		# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json",SCOPES)
			creds = flow.run_local_server(port=0)
	# Save the credentials for the next run
	with open('token.json', 'w') as token:
		token.write(creds.to_json())
	try:
		service = gspread.authorize(creds)
	except Exception as e:
		print("Error getting creds:")
		print(e)
		return None
	return service
def get_spreadsheet_id():
	return SPREADSHEET_ID
def upload():
	done = False
	service = main()
	sheet = service.open_by_key(SPREADSHEET_ID).get_worksheet(0)
	with open('items.csv','r',newline='') as f:
		#skips header
		reader = csv.reader(f)
		data = list(reader)[1:]
	#1. get length of items ,2. add rows (copy from first) with one or 2 spacer rows 3. fill data
	#Week,Item,USD,GBP,Sup-UK,gbp-myr,MYR,UK-MY (Shipping + Fee),ACO fee,Gross Price,Final Price (RM)
	try:
		formulas = []
		spacer = []
		for i in "efghijk":
			f = sheet.acell('{}1'.format(i), value_render_option='FORMULA').value
			formulas.append(str(f))
		n = 3
		for i in data:
			i.insert(0,"")
			i.extend([re.sub(r"(?<=[A-Z])\d",str(n),j) if "=" in j else j for j in formulas])
			n=n+1
		#Insert 2 spacer rows and insert rows with data
		week = int(sheet.acell("A3").value)
		new_week = week + 1
		sheet.insert_rows([[],[]],row=3,value_input_option="RAW")
		sheet.insert_rows(data, row=3, value_input_option='USER_ENTERED')
		sheet.update("A3",new_week)
		done = "DONE"
		# for i in range(len(data)+2):
		# 	spacer.append([])
		# sheet.insert_rows(spacer,row=3)
		#sheet.insert_rows(data, row=3, value_input_option='USER_ENTERED')
		# cell_list = sheet.range("A3:K{}".format(str(len(data)+3)))
		# for i,index in enumerate(cell_list):
		# 	i.value = data[index]
		# sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
	except Exception as e:
		done = e
	return done
def test():
	return "DONE"
if __name__ == "__main__":
	print(test())
	#upload()