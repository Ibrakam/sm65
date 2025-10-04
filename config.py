from dotenv import dotenv_values

config_values = dotenv_values(".env")

# {"ALGORITHM":HS256}

algorithm = config_values["ALGORITHM"]
secret_key = config_values["SECRET_KEY"]
access_token_exp_minutes = config_values["ACCESS_TOKEN_EXPIRE_MINUTES"]
