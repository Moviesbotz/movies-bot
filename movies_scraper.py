import requests
from bs4 import BeautifulSoup


url_list = {}
api_key = "45c5a4a773e132b44a5b2e9056d07befd949276e"


def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://185.53.88.104/?s={query.replace(' ', '+')}").text, "html.parser")
    movies = website.find_all("a", {'class': 'ml-mask jt'})
    for movie in movies:
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
            url_list[movies_details["id"]] = movie['href']
        movies_list.append(movies_details)
        movies_details = {}
    return movies_list


def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
    if movie_page_link:
        title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
        movie_details["title"] = title
        img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
        movie_details["img"] = img
        links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        final_links = {}
        for i in links:
            url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
            try:
                response = requests.get(url, timeout=30)
                link = response.json()
                final_links[f"{i.text}"] = link['shortenedUrl']
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while requesting URL shortener API: {e}")
                final_links[f"{i.text}"] = "Error: Unable to retrieve shortened URL"
        movie_details["links"] = final_links
    return movie_details
