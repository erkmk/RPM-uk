from flask import request
from controllers.auth import ClientAccess
from flask_jsonpify import jsonify


class Company(ClientAccess):
    def get(self, companyId):
        sql = "SELECT c.*,u.user_id,u.email,u.name FROM  company c LEFT JOIN user u ON u.company_id = c.company_id WHERE c.company_id = '" + \
            companyId + "'"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        header = mycursor.description
        # print(header)
        row_headers = [x[0] for x in mycursor.description]
        # mycursor.close()
        # print(row_headers)
        result = [dict(zip(row_headers, res)) for res in result]
        # users = {"message": result};
        print(result)
        return jsonify(result)


    def post(self,):
        company = request.json
        print(company)
        compId = company['company_id']
        del company['company_id']
        pairs = company.items()
        key = []
        value = []
        for k, v in pairs:
            key.append(str(k))
            value.append(str(v))
        key = tuple(key)
        value = tuple(value)
        print(value)
        if (compId == ""):
            try:
                sql = "INSERT INTO company (" + ", ".join(key) + \
                    ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql, value)
                mydb.commit()
            except Exception as e:
                print(e)
            # mycursor.close()

            sql = "SELECT LAST_INSERT_ID()"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                companyId = {"message": str(
                    mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
            # mycursor.close()
            except Exception as e:
                print(e)
            os.mkdir("/home/musab/RapidPMV2/artefacts/" + companyId["message"])
            return jsonify(companyId)
        else:
            sql = "UPDATE company SET RPM = '" + value[0] + "', company_name = '" + value[1] + "', contact_name = '" + value[
                2] + "', address_line1 = '" + value[
                3] + "', address_line2 = '" + value[4] + "', address_line3 = '" + value[5] + "', city = '" + value[
                6] + "',country = '" + \
                value[7] + "',postal_code = '" + value[8] + \
                "' WHERE company_id = '" + str(compId) + "';"
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
            companyId = {"message": str(compId)}
            return jsonify(companyId)
