def update_movie(payload) :
    query_to_update_movie = """
    mutation updateMovie($movie_id: String!, $customer_id: String!, $description: String, $genre_type: String, $release_date: String) {
        update_movies_table(where: {customer_id: {_eq: $customer_id}, movie_id: {_eq: $movie_id}}, _set: {genre_type: $genre_type, release_date: $release_date, description: $description}) {
            returning {
            customer_id
            }
            affected_rows
        }
    }
    """
    release_date = None
    description = None
    genre_type = None
    if 'genre_type' in payload and payload['genre_type'] != "" :
        genre_type = payload['genre_type']
    if 'description' in payload and payload['description'] != "" :
        description = payload['description']
    if 'release_date' in payload and payload['release_date'] != "" :
        release_date = payload['release_date']
    
    variables_to_update_movie = {
        "movie_id" : payload['movie_id'],
        "customer_id" : payload['customer_id'],
        "release_date" : release_date,
        "genre_type": genre_type,
        "description" : description
    }
    response_to_update_movie = {'query' : query_to_update_movie, "variables" : variables_to_update_movie}
    return response_to_update_movie