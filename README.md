# Web_Scraper_movies_sample
This code uses lxml and requests to simply extract a list of italian movies, genres, directors and actors from the "mymovies.it" website.
After selecting a year of interests at the beginning, it scrapes the pages from the website and download the information.
All information is visualized while scraping, then saved in csv format through the basic csv python module. 
Finally, the "films.csv" file can be imported to excel.

An updated version is to come shortly.
The new release will be able to:
- run over multiple years
- handle exceptions like multiple directors or no information
- save a more structured csv
