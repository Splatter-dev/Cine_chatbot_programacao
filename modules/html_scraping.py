from bs4 import BeautifulSoup
import requests
from datetime import datetime
from time import sleep
from modules.gc_bucket import download_blob, upload_blob



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

