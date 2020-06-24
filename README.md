# Web_Scraper_movies_sample
This code uses lxml and requests to simply extract a list of italian movies, genres, directors and actors from the "mymovies.it" website.
After selecting a year of interests at the beginning, it scrapes the pages from the website and download the information.
All information is visualized while scraping, then saved in csv format through the basic csv python module. 
Finally, the "films.csv" file can be imported to excel.
The main disadvantage is that directors and actors are appended as lists in a "cell". Thus, they are not searchable in a proper DB way.
To overcome this problem, we'd better use a DBMS instead of a csv, but this would drop this code simplicity. 
