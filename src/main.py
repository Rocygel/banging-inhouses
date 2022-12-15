#######################################################################
# Main file for the software used to organize data from inhouse games #
# provided by the Replay Book software made by fraxiinus. The file's  #
# main purpose is to push everything up to the Google Drive for       #
# public viewing.                                                     #
#######################################################################

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)
client = gspread.authorize(credentials)

# sheet = client.create("FirstSheet")

# sheet.share('rogmasterrc@gmail.com', perm_type='user', role='writer')

# run the other two scripts, reformatting and compiling raw data to be uploaded
# reformatter
# compiler

# edit editor (remove later)
sheet = client.open("BANGING INHOUSES").worksheet("TOP")
df = pd.read_csv('test1.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# top editor
sheet = client.open("BANGING INHOUSES").worksheet("TOP")
df = pd.read_csv('top.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# jungle editor
sheet = client.open("BANGING INHOUSES").worksheet("JUNGLE")
df = pd.read_csv('jungle.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# mid editor
sheet = client.open("BANGING INHOUSES").worksheet("MID")
df = pd.read_csv('mid.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# adc editor
sheet = client.open("BANGING INHOUSES").worksheet("ADC")
df = pd.read_csv('adc.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())

# support editor
sheet = client.open("BANGING INHOUSES").worksheet("SUPPORT")
df = pd.read_csv('support.csv')
sheet.update([df.columns.values.tolist()] + df.values.tolist())
