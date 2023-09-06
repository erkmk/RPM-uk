import jwt

def jwtToken(email, password):
    # define the payload data for jwt
    payload = { 'email': email, 'password': password}

    # Define the secret key to sign the jwt
    secret_key = 'AbraKaDabra'

    # generate the jwt token
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

    # print(jwt_token)

    return jwt_token

# if __name__ == '__main__':
#     jwtToken('sam@gmail.com','Alchemist21@#')