from modules.html_scraping import prog_date_extract
import datetime


def date_convert_ptbr():
   
    days_name_ptbr = ('Domingo','Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado')

    date_list_converted = []

    dates_from_site = prog_date_extract()
    
    for day in dates_from_site:
        
        date_splited = day.split('-')
        dia_esc = datetime.datetime(year=int(date_splited[0]), month=int(date_splited[1]),day=int(date_splited[2]))

        day_date = date_splited[2] + '/' + date_splited[1]

        day_week_name = ' - ' + days_name_ptbr[int(dia_esc.strftime('%w'))]

        date_list_converted.append(day_date + day_week_name)

    return date_list_converted
