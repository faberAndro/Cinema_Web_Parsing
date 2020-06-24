# TODO: RISCRIVERE TUTTO UTILIZZANDO "ITER"
# TODO: RISOLVERE IL PROBLEMA DEI REGISTI NULLI OPPURE MAGGIORI DI UNO
# TODO: PROCEDURA PER LA RICERCA DI TUTTI I FILM ITALIANI IN UN ANNO SPECIFICO (1960 IN QUESTO ESEMPIO)
# TODO: MODIFICARE LA RICERCA SEQUENZIALMENTE. IL REGISTA POTREBBE NON ESSERCI
from lxml import etree
from io import StringIO, BytesIO
import csv
import requests


def page_address_parameters():
    s = "https://www.mymovies.it/database/ricerca/avanzata/?"
    s += 'titolo='
    s += '&titolo_orig='
    s += '&regista='
    s += '&attore='
    s += '&id_genere=-1'
    s += '&nazione=' + str(nation)
    s += '&clausola1=%3D'
    s += '&anno_prod=' + str(year)
    s += '&clausola2=-1'
    s += '&stelle=-1'
    s += '&id_manif=-1'
    s += '&anno_manif='
    s += '&disponib=-1'
    s += '&ordinamento=0'
    s += '&submit=Inizia+ricerca+%C2%BB'
    return s
        

def analyse_year():
    list_over_this_year = []
    page_number = 1
    while True:
        dictionary_of_films_in_this_page = analyse_page(page_number)
        page_number += 1
        if dictionary_of_films_in_this_page:
            list_over_this_year.extend(dictionary_of_films_in_this_page)
        else:
            return list_over_this_year


def extract_page(current_page_number):
    if current_page_number != 1:
        url_to_download = indirizzo + "&page2&page=2&page=" + str(current_page_number)
    else:
        url_to_download = indirizzo + "&page"
    page_text = requests.get(url_to_download).text
    return page_text


def analyse_page(n_page):

    text_of_current_page = extract_page(n_page)
    list_of_dictionaries = []
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(text_of_current_page), parser)
    result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    films = tree.xpath('//h2/parent::div[@class="linkblu"]')
    n_films = len(films)
    if not n_films:
        return None

    for film in films:
        titolo = film.xpath('h2/a')[0].text
        registi = film.xpath('div/b/a/text()')
        attori_e_genere = film.xpath('div/a/text()')
        dictionary = {'year': attori_e_genere[-1],
                      'title': titolo,
                      'genre': attori_e_genere[-2],
                      'directors': registi,
                      'actors': attori_e_genere[:-2]
                      }
        list_of_dictionaries.append(dictionary)
    return list_of_dictionaries


def write_year_on_csv(lista_di_films):
    with open('films.csv', 'a', newline='') as csvfile:
        fieldnames = ['title', 'genre', 'year', 'directors', 'actors']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        for film in lista_di_films:
            writer.writerow(film)
        csvfile.close()


if __name__ == '__main__':
    nation = 'Italia'
    print('Nation: Italy')
    print('year range: [1905, 2020]')
    while True:
        y1 = input('Start year? ')
        y2 = input('End year? ')
        if y1.isdigit() and y2.isdigit():
            y_1, y_2 = int(y1), int(y2)
            if y_1 in range(1905, 2021) and y_2 in range(1905, 2021) and y_2 >= y_1:
                y_2 += 1
                break
            else:
                print('Invalid numbers. Please try again')
        else:
            print('Invalid numbers. Please try again')

    years = range(y_1, y_2)
    for year in years:
        indirizzo = page_address_parameters()
        lista_di_films = analyse_year()
        write_year_on_csv(lista_di_films)
    print('Movies extracted from %d to %d' % (y_1, y_2-1))
