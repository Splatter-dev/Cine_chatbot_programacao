from bs4 import BeautifulSoup
import base64
import requests
from datetime import datetime
from time import sleep
from google.cloud import storage


####################### SCRAPING ####################################################
def site_request():

    url = 'https://www.topaziocinemas.com.br/programacao'
    topazio_web_site_prog = requests.get(url).text
    sleep(3)

    return topazio_web_site_prog


def create_site_html_file():
    # cria arquivo com toda programação
    topazio_web_site_prog = site_request()
    site = BeautifulSoup(topazio_web_site_prog, 'lxml')

    # Remove entidade &nbsp dos hoŕarios dos filmes
    replace_string_nbsp = site.find_all(text=True)
    for text in replace_string_nbsp:
        newtext = text.replace("&nbsp", " ")
        text.replace_with(newtext)

    tab_content = site.find(class_='tab-content').prettify()
    upload_blob(tab_content, 'site.html')


def open_site_html_file():
    # abre arquivo com toda programação
    file = download_blob('site.html')
    site = BeautifulSoup(file, 'lxml')

    return site


def prog_date_extract():
    # extrai as datas dos dias de programação
    prog_days = []
    site = open_site_html_file()

    # Dia de hoje
    for tab in site.find_all(class_="tab-pane tabprog fade in active"):
        prog_days.append(tab.attrs['id'][4:])

    # Demais dias
    for tab in site.find_all(class_="tab-pane tabprog fade"):
        prog_days.append(tab.attrs['id'][4:])

    return prog_days


def create_prog_day_date_html_files():
    # Extrai programação criando um arquibo html para cada dia
    tim = datetime.time(datetime.now())
    print(tim)
    create_site_html_file()
    site = open_site_html_file()
    prog_days = prog_date_extract()

    for day in prog_days:
        selected_day = site.find(id=f"tab-{day}").prettify()
        upload_blob(selected_day, f'prog_day_{day}.html')


############################### BUCKET   ##############################
def connect_to_bucket():
    try:
        storage_client = storage.Client()
        bucket_name = "html_scraping"
        bucket = storage_client.bucket(bucket_name)
        return bucket
    except:
        raise ConnectionError('Erro ao conectar ao storage')


def upload_blob(source_file_name, destination_blob_name):

    bucket = connect_to_bucket()

    blob = bucket.blob(f'prog_days/{destination_blob_name}')

    try:
        blob.upload_from_string(source_file_name)
    except:
        raise ConnectionError('Falha ao fazer uplaod do arquivo')


def download_blob(source_file_name):

    bucket = connect_to_bucket()
    blob = bucket.blob(f'prog_days/{source_file_name}')

    try:
        blob_str = blob.download_as_text()
        return blob_str
    except:
        raise ConnectionError('Falha ao fazer download do arquivo.')


############ LISTEN TOPIC #####################

def do_scraping(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    try:
        if pubsub_message == 'DOIT':
            create_prog_day_date_html_files()
    except:
        raise ConnectionError('Erro ao conectar.')
