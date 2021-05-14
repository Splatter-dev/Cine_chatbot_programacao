from bs4 import BeautifulSoup
from modules.gc_bucket import download_blob
import re


def prog_day_to_open(date):

    file = download_blob(f'prog_day_{date}.html')
    prog_day = BeautifulSoup(file, 'lxml')

    return prog_day


def extract_movies_titles(html_file_opened):
    # extraindo titulos 
    prog_day =  html_file_opened
    movies = [movie.get_text("\n",strip=True) for movie in prog_day.find_all(class_="filme-tit")]
    return movies


def extract_class_row_class_session(html_file_opened):
    
    # extaindo class=row junto com class=sessao row
    prog_day =  html_file_opened
    class_row_and_sessao = []
    for row in prog_day.find_all(class_="row"):
        class_row_and_sessao.append(row.get_text(" ",strip=True))

    # extraindo class-row
    class_row = []
    for row_ag in class_row_and_sessao:
        if "Shopping Jaraguá Indaiatuba" in row_ag:
            class_row.append(row_ag)
    return class_row


def split_shopping_schedules(html_file_opened):

    class_row = extract_class_row_class_session(html_file_opened)

    # Separa programação do Polo e Jaraguá
    for index, info_session in enumerate(class_row):

        position_find_polo = info_session.find("Polo Shopping")
        index_inserted_polo = info_session[:position_find_polo] + '\n\n' + info_session[position_find_polo:]

        class_row.pop(index)
        class_row.insert(index, index_inserted_polo)

    splited_shopping_prog = class_row

    return splited_shopping_prog

def split_and_add_strong_to_shopping_name(class_row):
    
    # Quebra linha entre nome do shopping e versões/horários das sessões e adiciona <strong> - Jaraguá
    for index, info_session in enumerate(class_row):

        position_find_jrg, len_str_jrg = info_session.find("Shopping Jaraguá Indaiatuba"), len("Shopping Jaraguá Indaiatuba")
        
        index_inserted_polo = '<strong>' + info_session[:position_find_jrg + len_str_jrg].strip() + ':' + '</strong>'\
             + '\n' + info_session[len_str_jrg:].strip()
        class_row.pop(index)
        class_row.insert(index, index_inserted_polo)


    # Quebra linha entre nome do shopping e versões/horários das sessões - Polo
    for index, info_session in enumerate(class_row):

        position_find_polo, len_str_polo = info_session.find("Polo Shopping Indaiatuba"), len("Polo Shopping Indaiatuba")
    
        index_inserted_polo = info_session[:position_find_polo + len_str_polo].strip() \
            + ':' +'\n' + info_session[position_find_polo + len_str_polo:].strip() 
            
        class_row.pop(index)
        class_row.insert(index, index_inserted_polo)

    # Adiciona <strong> ao titulo do Polo Shopping Indaiatuba
    new_list_strong_polo = []
    for index, info_session in enumerate(class_row):

        partitioned_str = info_session.partition("Polo Shopping Indaiatuba:")
        partitioned_str_list = [part for part in partitioned_str]

        for index_part, part in enumerate (partitioned_str_list):
            if part == "Polo Shopping Indaiatuba:":
                updated__strong_str = "<strong>Polo Shopping Indaiatuba:</strong>"
                partitioned_str_list.pop(index_part)
                partitioned_str_list.insert(index_part, updated__strong_str)
        
        new_list_strong_polo.append(''.join(partitioned_str_list))

    class_row = new_list_strong_polo
    splitted_shopping_name = class_row[:]

    return splitted_shopping_name

def break_line_btw_vip_and_comfort(class_row):
    # Quebra linha entre as descrições de VIP e os horários das sessões
    for index, info_session in enumerate(class_row):

        position_find_vip = info_session.find("VIP = sessão na sala Topázio VIP do Polo Shopping")

        if position_find_vip != -1:
            elemento_atualizado = info_session[:position_find_vip] + '\n\n' + info_session[position_find_vip:]
            class_row.pop(index)
            class_row.insert(index,elemento_atualizado )

    # Quebra linha entre as descrições de Comfort e os horários das sessões
    for index, info_session in enumerate(class_row):

        position_find_comfort = info_session.find("TC = sessão na sala Topázio Comfort do Shopping Jaraguá")

        if position_find_comfort != -1:
            elemento_atualizado = info_session[:position_find_comfort] + '\n\n' + info_session[position_find_comfort:]
            class_row.pop(index)
            class_row.insert(index,elemento_atualizado)

    breaked_vip_comfort = class_row[:]
   
    return breaked_vip_comfort


def break_line_btw_movie_versions(class_row):
    # Quebra linha entre versões de filmes
    for loop in range(0,2):
        for index, info_session in enumerate(class_row):

            if ' 2D LEG' in info_session:
                pattern_sub =  re.compile(' 2D LEG')
                string_sub = pattern_sub.search(info_session)
                info_session_updated = info_session[:string_sub.start()] + '\n' + info_session[string_sub.start():].strip()
                class_row.pop(index)
                class_row.insert(index,info_session_updated)

            if ' 2D DUB' in info_session:
                pattern_dub =  re.compile(' 2D DUB')
                string_dub = pattern_dub.search(info_session)
                info_session_updated = info_session[:string_dub.start()] + '\n' + info_session[string_dub.start():].strip()
                class_row.pop(index)
                class_row.insert(index,info_session_updated)   

    breaked_movie_versions = class_row[:]
   
    return breaked_movie_versions


def join_titles_and_schedules(date):
# Juntar programação com os titulos dos filmesn

    html_date_file_opened = prog_day_to_open(date)

    splitted_shopping_schedules = split_shopping_schedules(html_date_file_opened)

    splitted_shopping_name =  split_and_add_strong_to_shopping_name(splitted_shopping_schedules)

    breaked_line_vip_comfort = break_line_btw_vip_and_comfort(splitted_shopping_name)

    movie_theaters_sessions = break_line_btw_movie_versions(breaked_line_vip_comfort)

    movies =  extract_movies_titles(html_date_file_opened)

    schedules_and_titles = []

    for index, movie in enumerate(movies):
        schedules_and_titles.append(
            '🍿 ' + '<strong>' + movie + '</strong>' + ' 🍿'
            + '\n\n' + movie_theaters_sessions[index])
    
    return schedules_and_titles

