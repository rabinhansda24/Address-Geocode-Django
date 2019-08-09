from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import json
import time
from GeoCode.functions import geocode
from GeoCode.forms.upload_form import UploadExcelForm
import pandas as pd
import django_excel as excel
import xlsxwriter


try:
    from io import BytesIO as IO # for modern python
except ImportError:
    from io import StringIO as IO # for legacy python



def index(request):
    form = UploadExcelForm()
    return render(request, 'GeoCode/upload.html', {'form': form})


def upload(request):
    if request.method == "POST":
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            # get the excel file from post request object
            filehandle = request.FILES['file']
            df = pd.read_excel(filehandle)
            # Convert it into pandas data frame
            data = pd.DataFrame(df)
            pd.options.display.max_colwidth = 100
            address_with_latlng = []
            dealy = 5
            # Iterate through the address in the excel
            for index, row in df.iterrows():
                # Calling the get_geocode function to get the GeoCode of an address
                lat, lang = geocode.get_geocode(row['Address'])
                latlng = 'lat:' + str(lat) + ', lang:' + str(lang)
                # Appending the newly aquired lat lang to the row
                row['LatLng'] = latlng
                # Appending the entire row in a new list

                address_with_latlng.append(row.tolist())

                # Dealying the API call by 5 sec to avoid google api policy
                time.sleep(dealy)
            final_df = pd.DataFrame(address_with_latlng)
            excel_file = IO()
            xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
            final_df.to_excel(xlwriter, 'Address')
            xlwriter.save()
            xlwriter.close()
            excel_file.seek(0)
            res = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            res['Content-Disposition'] = 'attachment; filename=address_with_lat_long.xlsx'
            return res
    else:
        form = UploadExcelForm()
    return render(request, 'GeoCode/upload.html', {'form': form})
