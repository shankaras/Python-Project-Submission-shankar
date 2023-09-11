import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_movies_by_genre(genre):
    url = "https://www.imdb.com/search/title/?genres=" + genre
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_titles = [title.text for title in soup.find_all('h3', class_='lister-item-header')]
        movie_ratings = [rating.text.strip() for rating in soup.find_all('span', class_='value')]
        movie_summaries = [summary.text.strip() for summary in soup.find_all('p', class_='text-muted')]
        movie_data = [{'Title': title, 'Rating': rating, 'Summary': summary} for title, rating, summary in zip(movie_titles, movie_ratings, movie_summaries)]

        if movie_data:
            return movie_data
        else:
            return None
    else:
        return None

def main():
    genre = input("Enter a movie genre: ")
    movie_data = scrape_movies_by_genre(genre)

    if movie_data:
        movie_df = pd.DataFrame(movie_data)
        movie_df.to_csv('movie_suggestions.csv', index=False)
        print("Movie suggestions:")
        for movie in movie_data:
            print(f"Title: {movie['Title']}")
            print(f"Rating: {movie['Rating']}")
            print(f"Summary: {movie['Summary']}")
            print("\n")
    else:
        print("Failed to fetch data or no movies found for the given genre.")

if __name__ == "__main__":
    main()
