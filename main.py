import psycopg2

def create_db(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(        
        id SERIAL PRIMARY KEY ,
        first_name VARCHAR(30),       
        last_name VARCHAR(40),
        email VARCHAR(200));
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(       
        number VARCHAR(15) PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id));
    """)
    conn.commit()

def add_new_customer(conn, first_name, last_name, email, number=None):
    cur.execute("""    
        INSERT INTO customers(first_name, last_name, email) VALUES (%s, %s, %s);
        """, (name, lastname, email))
    conn.commit()

def add_phone_number (cur, customer_id, number):
    cur.execute("""
        INSERT INTO phone_numbers(number, customer_id) VALUES (%s, %s);   
        """, (number, customer_id))
    return customer_id

def change_customer (cur, customer_id=None, first_name=None, last_name=None, email=None, number=None ):
    if first_name is not None:
        cur.execute("""            
            UPDATE customers SET first_name=%s WHERE  id=%s;
            """, (firstname, customer_id))
    if last_name is not None:
        cur.execute("""            
            UPDATE customers SET last_name=%s WHERE id=%s;
            """, (lastname, customer_id))
    if email is not None:
        cur.execute("""           
            UPDATE customers SET email=%s WHERE id=%s;
            """, (email, customer_id))
    if number is not None:
        add_phone_number(conn, cur, customer_id,number)
        cur.execute(""" 
            SELECT * FROM customers     
            """)
    print(cur.fetchall())

def delete_number(cur, customer_id, number):
    cur.execute("""
        DELETE FROM phone_numbers WHERE customer_id=%s and number=%s;       
        """, (customer_id, number))
    cur.execute("""
        SELECT FROM phone_numbers WHERE customer_id=%s;  
        """, (customer_id,))
    print(cur.fetchall())

def delete_customer(cur, customer_id):
    cur.execute("""
        DELETE FROM phone_numbers WHERE customer_id=%s;       
        """, (customer_id,))
    cur.execute("""        
        DELETE FROM customers WHERE id=%s;
        """, (customer_id,))
    cur.execute("""
        SELECT * FROM customers;       
         """)
    print(cur.fetchall())

def find_customer(cur, first_name=None, last_name=None, email=None, number=None):
    if number is not None:
        cur.execute("""           
            SELECT c.id FROM customers c
            JOIN phone_numbers pn ON pn.customer_id = c.id           
            WHERE pn.number=%s;
            """, (number))
    else:
        cur.execute("""           
            SELECT id FROM customers 
            WHERE first_name=%s OR last_name=%s OR email=%s;        
            """, (firstname, lastname, email))
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="customers_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            create_db(conn, cur)

conn.close()
