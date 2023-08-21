def create_user(payload) :
    query_to_create_user = """
    mutation createUser($name: String!, $email: String!, $phone_number: String!, $password: String!) {
        insert_customer(objects: {active_customer: true, name: $name, email: $email, phone_number: $phone_number, password: $password}) {
                affected_rows
                returning {
                    customer_id
            }
        }
    }
    """
    variables_to_create_user = {
        "name" : payload['name'],
        "phone_number" : payload['phone_number'],
        "email": payload['email'],
        "password" : payload['password']
    }
    response_to_create_user = {'query' : query_to_create_user, "variables" : variables_to_create_user}
    return response_to_create_user