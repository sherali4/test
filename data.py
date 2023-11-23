from datetime import date
import json
import urllib.request
import os
import csv
from config import ids

filename = f"siat-data-{date.today()}.xlsx"
csv_filename = f"siat-data-{date.today()}.csv"

try:
  os.remove(csv_filename)
except OSError:
  print(f"{csv_filename} not exists")

birinchi_satr = [
    'id', 'klassifikator_kodi', 'name_uz', 'name_ru', 'name_en', 'davr',
    'miqdor'
]

with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
  writer = csv.writer(f, delimiter=';')
  writer.writerow(birinchi_satr)
  for id in ids:
    url = f"https://api.siat.stat.uz/media/uploads/sdmx/sdmx_data_{id}.json"
    # with urllib.request.urlopen(
    #     f"https://api.siat.stat.uz/media/uploads/sdmx/sdmx_data_{id}.json"
    # ) as url:
    #   data = json.load(url)

    try:
      with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))

        for d in range(0, len(data[0]['metadata'])):
          for key, value in data[0]['data'][d].items():
            if value == data[0]['data'][d]['Code'] or value == data[0]['data'][
                d]['Klassifikator'] or value == data[0]['data'][d][
                    'Klassifikator_ru'] or value == data[0]['data'][d][
                        'Klassifikator_en']:
              pass
            else:
              miqdor = str(value).replace(".", ",")
              writer.writerow([
                  id,
                  data[0]['data'][d]['Code'],
                  data[0]['data'][d]['Klassifikator'],
                  data[0]['data'][d]['Klassifikator_ru'],
                  data[0]['data'][d]['Klassifikator_en'],
                  key,
                  miqdor,
              ])
    except:
      print(f"{id} - xatolik bor")

print('successfully')
