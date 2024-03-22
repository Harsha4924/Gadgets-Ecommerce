from django.db import connection
import base64

def get_all_products():
    audit_list=[]
    sqlString="""select * from products """
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString)
            for record in curs:
                id=record[0]
                product_name=record[1]
                category=record[2]
                price = record[3]
                description=record[4]
                image = record[5]
                image_base64 = base64.b64encode(image).decode('utf-8')
                audit_list.append({"id":id,"product_name":product_name,"category":category,"price":price,"description":description,"image":image_base64})

    except Exception as e:
        print(e)
    finally:
        curs.close()
    return audit_list

def adding_to_cart(product_id,user,quantity):
    sqlString = """insert into cart (user_id,product_id,quantity)
                values(%s,%s,%s)"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user,product_id,quantity])
            connection.commit()
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    
def my_cart_items(user_id):
    l=[]
    sqlString = """select cart.product_id,cart.quantity,products.product_name,products.category,products.product_price,products.product_description,products.product_image 
                    from cart left join products on cart.product_id = products.product_id 
                    where cart.user_id=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user_id])
            for record in curs:
                product_id = record[0]
                quantity = record[1]
                product_name = record[2]
                category = record[3]
                price = record[4]
                description = record[5]
                image=record[6]
                image_base64 = base64.b64encode(image).decode('utf-8')

                l.append({'product_id':product_id,'quantity':quantity,'product_name':product_name,'category':category,'price':price,'description':description,'image':image_base64})
            #print(l)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        curs.close()
    return l

def remove_product(user_id,product_id):
    sqlString = """delete from cart where user_id=%s and product_id=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user_id,product_id])
            connection.commit()
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        curs.close()


def fetch_order_id(user_id,total_price):
    sqlString = """insert into orders(user_id,totalprice)
                values(%s,%s) RETURNING id"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user_id,total_price])
            order_id = curs.fetchone()[0]
            print("check",order_id)
            connection.commit()
            return order_id
    except Exception as e:
        print("boom",e)
        return False
    finally:
        curs.close()

def insert_all_orders(order_id,user_id,product_id,quantity,product_name,payment):
    
    sqlString = """insert into all_users_orders (order_id,user_id,product_id,quantity,product_name,payment)
                values(%s,%s,%s,%s,%s,%s)"""
    
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[order_id,user_id,product_id,quantity,product_name,payment])
            connection.commit()
            return True
    except Exception as e:
        print("error",e)

def update_user_payment(user_id,order_id):
    sqlString = """update all_users_orders set payment=True where user_id=%s and order_id=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user_id,order_id])
            connection.commit()
            return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    
def retrieve_my_orders(user_id):
    sqlString = """select products.product_name,products.product_description,products.product_price,products.product_image from products 
                left join all_users_orders on products.product_id=all_users_orders.product_id 
                where user_id=%s and payment=true """
    l2=[]
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[user_id])
            for record in curs:
                product_name = record[0]
                product_des=record[1]
                product_price=record[2]
                product_image=record[3]
                product_images = base64.b64encode(product_image).decode('utf-8')

                l2.append({'product_name':product_name,'product_des':product_des,'product_price':product_price,'product_images':product_images})
    except Exception as e:
        print("An error occurred:", e)
    finally:
        curs.close()
    return l2




