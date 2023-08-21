def get_movie(payload) :
    query_to_get_movie = """
    query MyQuery($movie_name: String, $release_date: String, $genre_type: String) {
        movies_table(where: {genre_type: {_eq: $genre_type}, movie_name: {_eq: $movie_name}, release_date: {_eq: $release_date}}) {
            movie_id
            movie_name
            genre_type
            description
            release_date
        }
    }
    """
    release_date = None
    movie_name = None
    genre_type = None
    if 'genre_type' in payload and payload['genre_type'] != "" :
        genre_type = payload['genre_type']
    if 'movie_name' in payload and payload['movie_name'] != "" :
        movie_name = payload['movie_name']
    if 'release_date' in payload and payload['release_date'] != "" :
        release_date = payload['release_date']
    
    variables_to_get_movie = {
        "release_date" : release_date,
        "genre_type": genre_type,
        "movie_name" : movie_name
    }
    response_to_get_movie = {'query' : query_to_get_movie, "variables" : variables_to_get_movie}
    return response_to_get_movie