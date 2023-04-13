from  data_processor import models
import pandas as pd
import csv

def upload_data_db(received_url):
    try:
        file_data= pd.read_csv(received_url)
        for ind in file_data.index:
            obj=models.data(
                file_name=file_data['image_name'][ind],
                objects_detected=file_data['objects_detected'][ind],
                time_stamp=file_data['timestamp'][ind]
            )
            obj.save()
        return True
    except Exception as error:
        return False


def fetch_data_db(recevied_data):
    """
    select * from data
    where time_stamp > start_date and time_stamp < end_date
    """
    obj = models.data.objects.filter(time_stamp__range=[recevied_data.get('start_date'),recevied_data.get('end_date')]).\
        values('file_name', 'objects_detected', 'id')
    data_dict = {}
    for data in obj:
        obj_list = data['objects_detected'].split(',')
        for i in obj_list:
            if i in data_dict.keys():
                data_dict[i] = data_dict[i] + 1
            else:
                data_dict[i] = 1
    fields = ['Threat', 'Occurence']
    with open('result.csv','w',newline='') as file:
        writer=csv.DictWriter(file,data_dict.keys())
        writer.writeheader()
        writer.writerow(data_dict)
    return convert_to_html_table(['IMAGE NAME', 'DETECTIONS', 'IMAGE'], list(obj))


def convert_to_html_table(header, table_data: dict):
    html = "<table style=''><tr>"
    for inx, data in enumerate(table_data):
        if inx == 0:
            for row in header:
                html += f'<th>{row[0].upper() + row[1:]}</th>'
            html += '</tr><tr>'
            for row in data:
                if row=='id':
                    html+= f'<td><img width="50px" height="50px" src="static/images/{data["file_name"]}"></td>'
                else:
                    html += f'<td>{data[row] if data[row] != None else "N/A"}</td>'
            html += '</tr>'
        else:
            html += '<tr>'
            for row in data:
                if row=='id':
                    html+= f'<td><img width="50px" height="50px" src="static/images/{data["file_name"]}"></td>'
                else:
                    html += f'<td>{data[row] if data[row] != None else "N/A"}</td>'
            html += '</tr>'
    html += "</table>"
    return html

