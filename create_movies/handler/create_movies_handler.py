import json
import datetime
import logging
import requests
import re
from src import create_movie, movie_genre_exist

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_api_engine_config():
    hasura_endpoint = "https://temp-database.hasura.app/v1/graphql"
    return hasura_endpoint

def prepare_header():
    header = {'x-hasura-admin-secret': '5p0Qay2aQGGkqWpJV981BsiyrV40fEWBjcK5Fr48vRe4bTnBEXGWoLY51LmM47ru',
                  'Content-Type': 'application/json'}
    return header

def validate_request(payload) :
    response_code = 200
    response_msg = "Request processed successfully"
    print("validating request")
    
    required_fields = ['movie_id','description', 'customer_id', 'genre_type', 'release_date']
    
    for fields in required_fields :
        if not fields in payload or payload[fields] == "" :
            print("missing : ", fields)
            response_code = 400
            response_msg = "Request payload missing mandatory field(s)"
            return response_code, response_msg
        
    return response_code, response_msg

def lambda_handler(event, context) :
    logger.info(event)
    print("eventbody: ", event)
    error_codes = {
        'InvalidParameterException': {
            'message': 'Invalid parameter value format.',
            'code': '001',
        },
        'SomethingWentWrong': {
            'message' : 'Something went wrong',
            'code' : '002'
        },
        'GenreNotExist' : {
            'message' : 'Genre does not exist for given user',
            'code' : '004'
        },
        'MovieNotCreated' : {
            'message' : 'Some error occured while creating a new movie',
            'code' : '006'
        }
    }

    converted_response = {}
    is_request_valid_response_code, is_request_valid_response_msg = validate_request(event)

    if is_request_valid_response_code == 200 :
        try :
            hasura_endpoint = get_api_engine_config()
            hasura_header = prepare_header()
            query_response = None
            
            try :
                print("Trying to get a genre")
                query_response = movie_genre_exist(event['genre_type'], event['customer_id'])
                query_response = requests.post(hasura_endpoint, headers=hasura_header, json=query_response)
                query_response = query_response.json()
            except Exception as err:
                print("Something error occured while getting the genre :",err)
                converted_response['response_code'] = 400
                converted_response['response_error_code'] = error_codes['SomethingWentWrong']['code']
                converted_response['response_error_message'] = error_codes['SomethingWentWrong']['message']
                return build_response(converted_response, context)

            try: 
                print("Trying to get the genre id")
                print("query response ", query_response)
                query_response = query_response['data']
                query_response = query_response['genres']
                if len(query_response) == 0:
                    converted_response['response_code'] = 400
                    converted_response['response_error_code'] = error_codes['GenreNotExist']['code']
                    converted_response['response_error_message'] = error_codes['GenreNotExist']['message']
                    return build_response(converted_response, context)
            except Exception as err :
                print("Some error occured while getting the genre_id: ", err)
                converted_response['response_code'] = 400
                converted_response['response_error_code'] = error_codes['SomethingWentWrong']['code']
                converted_response['response_error_message'] = error_codes['SomethingWentWrong']['message']
                return build_response(converted_response, context)
            
            try :
                print("Trying to create a movie")
                query_response = create_movie(event)
                query_response = requests.post(hasura_endpoint, headers=hasura_header, json=query_response)
                query_response = query_response.json()
            except Exception as err:
                print("Something error occured while creating the movie :",err)
                converted_response['response_code'] = 400
                converted_response['response_error_code'] = error_codes['SomethingWentWrong']['code']
                converted_response['response_error_message'] = error_codes['SomethingWentWrong']['message']
                return build_response(converted_response, context)

            try: 
                print("Trying to get the movie id")
                print("query response ", query_response)
                query_response = query_response['data']
                query_response = query_response['insert_movies_table']
                affected_rows = query_response['affected_rows']
                if affected_rows == 1:
                    query_response = query_response['returning']
                    query_response = query_response[0]
                    movie_id = query_response['movie_id']
                    converted_response['response_code'] = 200
                    converted_response['response_message'] = is_request_valid_response_msg
                    return build_response(converted_response, context, movie_id)
                else :
                    converted_response['response_code'] = 200
                    converted_response['response_error_code'] = error_codes['MovieNotCreated']['code']
                    converted_response['response_error_message'] = error_codes['MovieNotCreated']['message']
                    return build_response(converted_response, context)
            except Exception as err :
                print("Some error occured while getting the genre_id: ", err)
                converted_response['response_code'] = 400
                converted_response['response_error_code'] = error_codes['SomethingWentWrong']['code']
                converted_response['response_error_message'] = error_codes['SomethingWentWrong']['message']
                return build_response(converted_response, context)

        except Exception as err:
            print("Something went wrong: ", err)
            converted_response['response_code'] = 400
            converted_response['response_error_code'] = error_codes['SomethingWentWrong']['code']
            converted_response['response_error_message'] = error_codes['SomethingWentWrong']['message']
            return build_response(converted_response, context)
    
    else :
        converted_response['response_code'] = is_request_valid_response_code
        converted_response['response_error_code'] = error_codes['InvalidParameterException']['code']
        converted_response['response_error_message'] = error_codes['InvalidParameterException']['message']
        converted_response['response_message'] = is_request_valid_response_msg
        return build_response(converted_response, context)
    
def build_response(converted_response, context, genre_id=None) :
    converted_response["request_id"] = context.aws_request_id
    converted_response["time_taken"] = str(context.get_remaining_time_in_millis())
    converted_response["request_timestamp"] = (
        datetime.datetime.now().astimezone().isoformat(timespec="milliseconds")
    )
    converted_response["response_data"] = {}
    if not genre_id is None:
        converted_response['genre_id'] = genre_id
        
    print("Converted response " , converted_response)
    return converted_response