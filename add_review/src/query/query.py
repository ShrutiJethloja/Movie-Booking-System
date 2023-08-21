def add_reviews(payload) :
    query_to_add_reviews = """
    mutation addReviews($customer_id: String!, $movie_id: String!, $reviews: String!, $ratings: String!) {
        insert_reviews(objects: {customer_id: $customer_id, movie_id: $movie_id, ratings: $ratings, reviews: $reviews}) {
            affected_rows
            returning {
            review_id
            }
        }
    }
    """
    variables_to_add_reviews = {
        "customer_id" : payload['customer_id'],
        "movie_id" : payload['movie_id'],
        "reviews" : payload['reviews'],
        "ratings" : payload['ratings']
    }
    response_to_add_reviews= {'query' : query_to_add_reviews, "variables" : query_to_add_reviews}
    return response_to_add_reviews