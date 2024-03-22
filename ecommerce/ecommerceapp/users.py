
import json
from django.db import connection
from . import utils

def get_user(email):
    sqlString = """select username from users where username=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[email])
            result = curs.fetchone()
            return result
    except Exception as e:
        print("An error occurred:", e)

def update_users(email,password):
    sqlString = """insert into users (username,password,status)
                   values (%s,%s,FALSE)"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[email,password])
            connection.commit()
            return 1
    except Exception as e:
        print("An error occurred:", e)

# def get_user_details(email,password):
#     sqlString = """select id, status from users where username=%s and password=%s"""
#     try:
#         with connection.cursor() as curs:
#             curs.execute(sqlString,[email,password])
#             result = curs.fetchone()
#             if result[1]:
#                 return result[0]
#             else:
#                 return False
#     except Exception as e:
#         print("An error occurred:", e)
        
def get_user_details(email,password):
    sqlString = """select id,status,password from users where username=%s"""

    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[email])
            result = curs.fetchone()
            if result[1]:
                verify_password = utils.verify(password,result[2])
                if verify_password:
                    print("boom its here")
                    return result[0]
            else:
                return False
    except Exception as e:
        print(e)
    finally:
        curs.close()
                

def get_details(email):
    sqlString = """select id,username,status from users where username=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[email])
            result = curs.fetchone()
            return {'id': result[0], 'email':result[1],'status':result[2]}
    except Exception as e:
        print("An error occurred:", e)

def get_user_id(uid):
    sqlString="""select * from users where id=%s"""
    try:

        with connection.cursor() as curs:
            curs.execute(sqlString,[uid])
            result = curs.fetchone()
            return {'id': result[0], 'email':result[1],'status':result[3]}
    except Exception as e:
        print(e)

def get_user_email(uid):
    sqlString="""select username from users where id=%s"""
    try:

        with connection.cursor() as curs:
            curs.execute(sqlString,[uid])
            result = curs.fetchone()
            return result
    except Exception as e:
        print(e)

def make_status_active(user):
    sqlString="""UPDATE users SET status = TRUE WHERE id = %s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user])
            result = curs.fetchone()
            print("checked")
            return result
    except Exception as e:
        print(e)
    
    
        