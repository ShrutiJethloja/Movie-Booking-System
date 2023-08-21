def create_movie(payload) :
    query_to_create_movie = """
    mutation createMovies($customer_id: String!, $movie_name: String!, $genre_type: String!, $description: String!, $release_date: String!) {
        insert_movies_table(objects: {customer_id: $customer_id, genre_type: $genre_type, movie_name: $movie_name description: $description, release_date: $release_date}) {
            affected_rows
            returning {
                movie_id
            }
        }
    }
    """
    variables_to_create_movie = {
        "customer_id" : payload['customer_id'],
        "genre_type" : payload['genre_type'],
        "description": payload['description'],
        "release_date" : payload['release_date'],
        "movie_name": payload['movie_name']
    }
    response_to_create_movie = {'query' : query_to_create_movie, "variables" : variables_to_create_movie}
    return response_to_create_movie

def movie_genre_exist(genre_type, customer_id) :
    query_to_get_genre_type = """
    query MyQuery($genre_type: String!, $customer_id: String!) {
        genres(where: {genre_type: {_eq: $genre_type}, customer_id: {_eq: $customer_id}}) {
            genre_id
        }
    }
    """
    variables_to_get_genre_type = {
        "customer_id" : customer_id,
        "genre_type" : genre_type
    }
    response_to_get_genre = {'query' : query_to_get_genre_type, 'variables' : variables_to_get_genre_type}
    return response_to_get_genre