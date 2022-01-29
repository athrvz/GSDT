from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.views import APIView 

import gspread

gc = gspread.service_account(filename='./gsdt_creds1.json')

# # configuring the DB -> Track worksheet 
# worksheet_db_track = gc.open('DB for email shortlister').worksheet('Track')
# # configuring the Copy worksheet
# # worksheet_copy = gc.open('Copy of GP for email shortlister').sheet1

################## Main Data Transfering implementation #################



# configuring the DB -> Track worksheet 
worksheet_db = gc.open('testDB').sheet1

# col no. for the 'website' col = 1
# row_values will give list in which website col will be at 0
website_index_db = 0
website_index_copy = 0
available_sheets_dic = {"4H": 2, "Mobi": 3}
# available_sheets = ["4H", "Mobi"]

def transfer_data_to(sheet_name):
    # configuring the Copy worksheet
    worksheet_copy = gc.open('testCopy').worksheet(sheet_name)
        
    for i in range(2, worksheet_db.row_count):
        found = False
        row_db = worksheet_db.row_values(i)
        # print("row_db: ", row_db)
        if not row_db: # empty row
            break
        website = row_db[website_index_db]
        # print("website: ", website)
        for j in range(2, worksheet_copy.row_count):
            if found:
                break
            row_copy = worksheet_copy.row_values(j)
            # print("row_copy: ", row_copy)
            if not row_copy:
                break
            website_ = row_copy[website_index_copy]
            # print("website_: ", website_)
            if website != website_:
                continue
            elif website == website_:
                found = True
        if not found:
            # print("not found")
            worksheet_copy.insert_row([website], i)
            worksheet_db.update_cell(i, available_sheets_dic[sheet_name], "YES")







################## Main Data Transfering implementation #################








# Create your views here.
# available_sheets = ["4H", "Mobi", "One", "TW", "TH", "IPRL", "App", "T+", "CT", "VE", "AMT", "MPF", "FP", "Can"]
available_sheets = ["4H", "Mobi"]
def index(request):
    return render(request, 'index.html')

    

class MyView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        sheet_name = self.kwargs.get('request_sheet')
        if sheet_name in available_sheets:
            if sheet_name == "Tplus":
                sheet_name = "T+"
            print("sheet_name: ", sheet_name)
            transfer_data_to(sheet_name)
        return HttpResponse(sheet_name)


    


# def function_name(request, url_parameter):
#     return render(request, 'Django Template', {url_parameter})