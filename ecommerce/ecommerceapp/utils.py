from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils.encoding import force_bytes, force_str

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,primary_key,timestamp):
        print("checking",primary_key)
        assert isinstance(primary_key, dict)
        return (six.text_type(primary_key['id'])+six.text_type(timestamp)+six.text_type(primary_key['status']))
        # return (force_str(primary_key['id']) + force_str(timestamp) + force_str(primary_key['status']))
generate_token=TokenGenerator()



def hash_it(password):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, primary_key, timestamp):
#         if isinstance(primary_key, dict):
#             return (six.text_type(primary_key.get('id', '')) +
#                     six.text_type(timestamp) +
#                     six.text_type(primary_key.get('status', '')))
#         elif isinstance(primary_key, int):
#             return (six.text_type(primary_key) +
#                     six.text_type(timestamp))
#         # Handle other types of primary_key if necessary
#         else:
#             # Return a default hash value or raise an error
#             raise ValueError("Unsupported type for primary_key")
# generate_token=TokenGenerator()

