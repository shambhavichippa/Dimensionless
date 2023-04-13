import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from data_processor.db_operations import upload_data_db, fetch_data_db
from django.core.files.storage import FileSystemStorage
from data_analyzer.settings import BASE_DIR
import pandas as pd

# Create your views here.
def landing_page(request):
    return render(request,'landing_page.html')

def upload_file(request):
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return render(request, 'landing_page.html', {'error_msg': 'Please upload csv file only'})
        save_file=FileSystemStorage()
        file=save_file.save(csv_file.name, csv_file)
        status = upload_data_db(BASE_DIR+"\\"+save_file.url(file))
        if status:
           return render(request, 'landing_page.html', {'success_msg': 'Uploaded Successfully'})
        else:
            return render(request, 'landing_page.html', {'error_msg': 'Something went wrong'})
    except Exception as error:
        print(error)
        import sys
        print("Line number of error {}".format(sys.exc_info()[-1].tb_lineno))
        print(">>>>>> error", error)
        return render(request, 'landing_page.html', {'error_msg': error})

class fetch_data(APIView):
    def post(self,request):
        response = {"is_success": False, "response_message": "", "data": {}, "response_code": 500}
        # data assign from response
        received_data = request.data
        final_data = fetch_data_db(received_data)
        response['data']=final_data
        response['is_success']=True
        response['response_code']=200
        result = json.dumps(response)
        return HttpResponse(result, status=200)
