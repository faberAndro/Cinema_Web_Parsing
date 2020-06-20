# TODO: RISCRIVERE TUTTO UTILIZZANDO "ITER"
# TODO: RISOLVERE IL PROBLEMA DEI REGISTI NULLI OPPURE MAGGIORI DI UNO
# TODO: PROCEDURA PER LA RICERCA DI TUTTI I FILM ITALIANI IN UN ANNO SPECIFICO (1960 IN QUESTO ESEMPIO)
# TODO: MODIFICARE LA RICERCA SEQUENZIALMENTE. IL REGISTA POTREBBE NON ESSERCI
from lxml import html
import csv
import time
import requests


def page_address_parameters():
    s = "https://www.mymovies.it/database/ricerca/avanzata/?"
    s += 'titolo='
    s += '&titolo_orig='
    s += '&regista='
    s += '&attore='
    s += '&id_genere=-1'
    s += '&nazione=Italia'
    s += '&clausola1=%3D'
    s += '&anno_prod=' + str(current_year)
    s += '&clausola2=-1'
    s += '&stelle=-1'
    s += '&id_manif=-1'
    s += '&anno_manif='
    s += '&disponib=-1'
    s += '&ordinamento=0'
    s += '&submit=Inizia+ricerca+%C2%BB'
    return s
        

def extract_page(current_page_number):
    if current_page_number != 1:
        url_to_download = indirizzo + "&page2&page=2&page=" + str(current_page_number)
    else:
        url_to_download = indirizzo + "&page"
    page_text = requests.get(url_to_download).text
    return page_text


def find_descriptive_parameters(first_page_text):
    v1, v2 = first_page_text.find("Hai cercato"), first_page_text.find("Ho trovato")
    i, punto = 0, False
    while not punto:
        if first_page_text[v2 + 1 + i] == ".":
            v3 = v2 + 1 + i
            punto = True
        i += 1
    u = first_page_text[v2:v3]
    z = u[(len("Ho trovato")):len(u)]
    x = z.split()[0]
    y = 0
    if x.isdigit():
        y = int(x)
    text_to_print = first_page_text[v1:v3 + 1]
    return text_to_print, y


def write_page_result_in_csv_file(file_di_output, *args):
    film_file = csv.writer(file_di_output, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    pagina = "page " + str(page_number)
    riga = [args[0]] + [args[1]] + [args[2]] + args[3]
    riga.insert(0, pagina)
    film_file.writerow(riga)


if __name__ == '__main__':
    current_year = None     # 1950 è ok
    page_number = 0
    n_results_in_current_year, n_films, all_TITLES_in_page, last_page = 0, 0, [], False     # last_page e' la last_page delle pagine relative all'anno corrente

    current_year = input('Anno? ')
    current_year = int(current_year)
    indirizzo = page_address_parameters()

    with open('films.csv', 'w', newline='') as file_di_output:
        while not last_page:
            page_number += 1
            text_of_current_page = extract_page(page_number)
            if page_number == 1:
                header, n_results_in_current_year = find_descriptive_parameters(text_of_current_page)
                print(header, n_results_in_current_year)
            tree = html.fromstring(text_of_current_page)
            all_TITLES_in_page = tree.xpath('//h2/a//@title')
            all_DIRECTORS_in_page = tree.xpath('//b//a[@href]/text()')
            actors_and_genres = tree.xpath('//div[contains(text(),"Un film di")]/a[@href]/text()')
            attori = []
            """
            ORA CONTA I FILM TROVATI E QUANTI NE RIMANGONO
            n_films = NUMERO DEI FILM TROVATI NELLA PAGINA
            n_results_in_current_year = NUMERO DEI FILM RIMANENTI
            CONTROLLA QUINDI A CHE PUNTO SIAMO
            """
            n_films = len(all_TITLES_in_page)
            n_results_in_current_year -= n_films
            print("\nPagina: %d -- Numero films: %d -- Film rimanenti nell'anno %d: %d" % (page_number, n_films, current_year, n_results_in_current_year))
            time.sleep(1)
            i, j = 0, 0
            for i in range(len(actors_and_genres)):
                k = actors_and_genres[i]
                if k != str(current_year):
                    attori.append(actors_and_genres[i])
                else:
                    genere = attori[len(attori)-1]
                    attori.remove(genere)
                    print("\n*** FILM: %s\n** REGISTA: %s\n**** ATTORI [%s]:  %s\n* GENERE: %s" %
                          (all_TITLES_in_page[j], all_DIRECTORS_in_page[j], len(attori), ', '.join(attori), genere))
                    write_page_result_in_csv_file(file_di_output, all_TITLES_in_page[j], all_DIRECTORS_in_page[j], genere, attori)
                    attori.clear()
                    j +=1
            if n_results_in_current_year == 0:
                last_page = True
    file_di_output.close()
