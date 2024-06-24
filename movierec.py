from collections import defaultdict

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    movie_ratings_dict = {}
    with open(f, 'r') as file:
        for line in file:
            movie, rating, user_id = line.strip().split('|')
            if movie not in movie_ratings_dict:
                   movie_ratings_dict[movie] = []
            movie_ratings_dict[movie].append(float(rating))
    return movie_ratings_dict

# 1.2
def read_movie_genre(f):
    movie_genre_dict = {}
    with open(f, 'r') as file:
        for line in file:
            genre, movie_id, movie = line.strip().split('|')
            movie_genre_dict[movie] = genre
    return movie_genre_dict

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(movie_to_genre):
    genre_dict = {}
    for movie, genre in movie_to_genre.items():
        if genre not in genre_dict:
            genre_dict[genre] = []
        genre_dict[genre].append(movie)
    return genre_dict

# 2.2
def calculate_average_rating(ratings_dict):
    avg_ratings_dict = {}
    for movie, ratings in ratings_dict.items():
        avg_ratings_dict[movie] = sum(ratings) / len(ratings)
    return avg_ratings_dict

# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(movie_avg_ratings, n=10):
    sorted_movies = sorted(movie_avg_ratings.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_movies[:n])

# 3.2
def filter_movies(movie_avg_ratings, threshold=3):
    return {movie: rating for movie, rating in movie_avg_ratings.items() if rating >= threshold}

# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_avg_ratings, n=5):
    movies_in_genre = genre_to_movies.get(genre, [])
    movies_avg_ratings = {movie: movie_avg_ratings[movie] for movie in movies_in_genre}
    sorted_movies = sorted(movies_avg_ratings.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_movies[:n])

# 3.4
def get_genre_rating(genre, genre_to_movies, movie_avg_ratings):
    movies_in_genre = genre_to_movies.get(genre, [])
    genre_avg_rating = sum(movie_avg_ratings[movie] for movie in movies_in_genre) / len(movies_in_genre)
    return genre_avg_rating

# 3.5
def genre_popularity(genre_to_movies, movie_avg_ratings, n=5):
    genre_avg_ratings = {genre: get_genre_rating(genre, genre_to_movies, movie_avg_ratings)
                         for genre in genre_to_movies.keys()}
    sorted_genres = sorted(genre_avg_ratings.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_genres[:n])

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(ratings_file):
    user_ratings_dict = {}
    with open(ratings_file, 'r') as file:
        for line in file:
            movie, rating, user_id = line.strip().split('|')
            if user_id not in user_ratings_dict:
                user_ratings_dict[user_id] = []
            user_ratings_dict[user_id].append((movie, float(rating)))
    return user_ratings_dict

# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    user_ratings = user_to_movies.get(user_id, [])
    genre_ratings = {}
    for movie, rating in user_ratings:
        genre = movie_to_genre.get(movie, None)
        if genre:
            if genre not in genre_ratings:
                genre_ratings[genre] = []
            genre_ratings[genre].append(rating)
    if not genre_ratings:
        return None
    return max(genre_ratings, key=lambda x: sum(genre_ratings[x]) / len(genre_ratings[x]))

# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_avg_ratings):
    user_ratings = user_to_movies.get(user_id, [])
    user_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    if not user_genre:
        return None

    unrated_movies = [movie for movie in movie_to_genre.keys() if movie not in dict(user_ratings)]
    genre_movies = [movie for movie, genre in movie_to_genre.items() if genre == user_genre]

    recommended_movies = [movie for movie in unrated_movies if movie in genre_movies]
    recommended_movies = sorted(recommended_movies, key=lambda x: movie_avg_ratings[x], reverse=True)

    return {movie: movie_avg_ratings[movie] for movie in recommended_movies[:3]}


def main():
    ratings_file = 'myratings.txt'
    movies_file = 'movies.txt'

   
    ratings_dict = read_ratings_data(ratings_file)
    movie_to_genre = read_movie_genre(movies_file)

   
    genre_to_movies = create_genre_dict(movie_to_genre)
    movie_avg_ratings = calculate_average_rating(ratings_dict)

  
    popular_movies = get_popular_movies(movie_avg_ratings)
    filtered_movies = filter_movies(movie_avg_ratings, 3)
    popular_in_genre = get_popular_in_genre('Action', genre_to_movies, movie_avg_ratings)
    genre_rating = get_genre_rating('Action', genre_to_movies, movie_avg_ratings)
    genre_popularity_result = genre_popularity(genre_to_movies, movie_avg_ratings)
    
  
    user_to_movies = read_user_ratings(ratings_file)
    user_genre = get_user_genre('1', user_to_movies, movie_to_genre)
    recommended_movies = recommend_movies('1', user_to_movies, movie_to_genre, movie_avg_ratings)

   #Results
    print("Task 1:")
    print("Ratings Dictionary:", ratings_dict)
    print("\n")
    print("Movie to Genre Dictionary:", movie_to_genre)

    print("\nTask 2:")
    print("Genre to Movies Dictionary:", genre_to_movies)
    print("\n")
    print("Movie Average Ratings Dictionary:", movie_avg_ratings)

    print("\nTask 3:")
    print("Popular Movies:", popular_movies)
    print("\n")
    print("Filtered Movies:", filtered_movies)
    print("\n")
    print("Popular in Genre:", popular_in_genre)
    print("\n")
    print("Average Rating in Genre:", genre_rating)
    print("\n")
    print("Genre Popularity:", genre_popularity_result)

    print("\nTask 4:")
    print("User to Movies Dictionary:", user_to_movies)
    print("\n")
    print("Top Genre for User 1:", user_genre)
    print("\n")
    print("Recommended Movies for User 1:", recommended_movies)
    
if __name__ == "__main__":
    main()