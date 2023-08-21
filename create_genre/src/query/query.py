def create_genre(payload) :
    query_to_create_genre = """
    mutation createGenre($customer_id: String!, $genre_type: String!) {
        insert_genres(objects: {customer_id: $customer_id, genre_type: $genre_type}) {
            affected_rows
            returning {
                customer_id
            }
        }
    }
    """
    variables_to_create_genre = {
        "customer_id" : payload['customer_id'],
        "genre_type" : payload['genre_type']
    }
    response_to_create_genre = {'query' : query_to_create_genre, "variables" : variables_to_create_genre}
    return response_to_create_genre