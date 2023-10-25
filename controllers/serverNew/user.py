from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class User(ClientAccess):
    def post(self):
        customer = request.json
        print(customer)
        custmId = customer['user_id']
        del customer['user_id']
        pairs = customer.items()
        key = []
        value = []
        for k, v in pairs:
            key.append(str(k))
            value.append(str(v))
        key = tuple(key)
        value = tuple(value)
        print(value)
        if (custmId == ""):
            sql = "INSERT INTO user (" + ", ".join(key) + \
                ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql, value)
                mydb.commit()
            # mycursor.close()
            except Exception as e:
                print(e)
            sql = "SELECT LAST_INSERT_ID()"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                customerId = {"message": str(
                    mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
            # mycursor.close()
            except Exception as e:
                print(e)
            return jsonify(customerId)
        else:
            sql = "UPDATE user SET company_id = '" + customer['company_id'] + "', company_role = '" + customer[
                'company_role'] + "', email = '" + customer['email'] + "', name = '" + customer['name'] + "', password = '" + \
                customer['password'] + "', status = '" + customer['status'] + "',verified = '" + customer[
                'verified'] + "' WHERE user_id = '" + str(custmId) + "';"
            # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                mydb.commit()
                # mycursor.close()
            except Exception as e:
                print(e)
            customerId = {"message": str(custmId)}
            return jsonify(customerId)