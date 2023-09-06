import mysql.connector
from os import listdir

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database = "RPMnew_dataBase",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS company (company_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "RPM VARCHAR(255) , "
                                                        "company_name VARCHAR(255), "
                                                        "contact_name VARCHAR(255), "
                                                        "address_line1 VARCHAR(255), "
                                                        "address_line2 VARCHAR(255), "
                                                        "address_line3 VARCHAR(255), "
                                                        "city VARCHAR(255), "
                                                        "country VARCHAR(255), "
                                                        "postal_code VARCHAR(255))")
mycursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "email VARCHAR(255) , "
                                                        "password VARCHAR(255), "
                                                        "company_role VARCHAR(255), "
                                                        "name VARCHAR(255), "
                                                        "status VARCHAR(255), "
                                                        "verified VARCHAR(255), "
                                                        "company_id INT, "
                                                        "FOREIGN KEY (company_id ) REFERENCES company(company_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS projects (project_id INT AUTO_INCREMENT PRIMARY KEY, "
#                                                         "ProjectType VARCHAR(255), "
#                                                         "ProjectTitle VARCHAR(255), "
#                                                         "ProjectDescription VARCHAR(255), "
#                                                         "ProjectStart VARCHAR(255), "
#                                                         "ProjectEnd VARCHAR(255), "
#                                                         "customer_id INT, "
#                                                         "CustomerEmail VARCHAR(255), "
#                                                         "FOREIGN KEY (customer_id) REFERENCES customers(customer_id))")

mycursor.execute("CREATE TABLE IF NOT EXISTS hierarchy_list (hierarchy_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "hierarchy_name VARCHAR(255))")

mycursor.execute("CREATE TABLE IF NOT EXISTS project (project_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "company_id INT, "
                                                        "project_name VARCHAR(255), "
                                                        "template VARCHAR(255), "
                                                        "status VARCHAR(255), "
                                                        "owner VARCHAR(255), "
                                                        "start VARCHAR(255), "
                                                        "end VARCHAR(255), "
                                                        "hierarchy_id_default VARCHAR(255), "
                                                        "FOREIGN KEY (company_id) REFERENCES company(company_id))")

# mycursor.execute("CREATE TABLE IF NOT EXISTS projects_artefactTypeDefault (artefactType_id INT AUTO_INCREMENT PRIMARY KEY, "
#                                                         "ArtefactType VARCHAR(255), "
#                                                         "TemplateUrl VARCHAR(255), "
#                                                         "LocationUrl VARCHAR(255), "
#                                                         "Manadatory VARCHAR(255), "
#                                                         "Multiples VARCHAR(255), "
#                                                         "project_id INT, "
#                                                         "FOREIGN KEY (project_id) REFERENCES projects(project_id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS hierarchy_container (container_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "container_title VARCHAR(255), "
                                                        "project_id INT, "
                                                        "hierarchy_id INT, "
                                                        "parent_container_id INT, "
                                                        "FOREIGN KEY (hierarchy_id) REFERENCES hierarchy_list(hierarchy_id), "
                                                        "FOREIGN KEY (project_id) REFERENCES project(project_id))")

mycursor.execute("CREATE TABLE IF NOT EXISTS artefact (artefact_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "artefact_type VARCHAR(255), "
                                                        "artefact_owner VARCHAR(255), "
                                                        "artefact_name VARCHAR(255), "
                                                        "description VARCHAR(255), "
                                                        "status VARCHAR(255), "
                                                        "create_date VARCHAR(255), "
                                                        "update_date VARCHAR(255), "
                                                        "location_url VARCHAR(255), "
                                                        "template_url VARCHAR(255), "
                                                        "project_id INT, "
                                                        "FOREIGN KEY (project_id) REFERENCES project(project_id), "
                                                        "template VARCHAR(255)) ")

mycursor.execute("CREATE TABLE IF NOT EXISTS container_artefact_link (link_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "container_id INT, "
                                                        "artefact_id INT, "
                                                        "FOREIGN KEY (artefact_id) REFERENCES artefact(artefact_id), "
                                                        "FOREIGN KEY (container_id) REFERENCES hierarchy_container(container_id))")

mycursor.execute("CREATE TABLE IF NOT EXISTS artefact_type_default (type_id INT AUTO_INCREMENT PRIMARY KEY, "
                                                        "project_id INT, "
                                                        "artefact_type VARCHAR(255), "
                                                        "location_url VARCHAR(255), "
                                                        "template_url VARCHAR(255), "
                                                        "multiples VARCHAR(255), "
                                                        "mandatory VARCHAR(255), "
                                                        "FOREIGN KEY (project_id) REFERENCES project(project_id))")
mycursor.execute("ALTER TABLE project_artefact_type_defaults MODIFY COLUMN id INT AUTO_INCREMENT")
# mycursor.execute("CREATE TABLE IF NOT EXISTS artifacts (artifact_id INT AUTO_INCREMENT PRIMARY KEY, "
#                                                         "ArtefactName VARCHAR(255), "
#                                                         "ArtefactType VARCHAR(255), "
#                                                         "ArtefactProductType VARCHAR(255), "
#                                                         "ArtefactStatus VARCHAR(255), "
#                                                         "Manadatory VARCHAR(255), "
#                                                         "Multiples VARCHAR(255), "
#                                                         "DateCreated VARCHAR(255), "
#                                                         "TemplateUrl VARCHAR(255), "
#                                                         "LocationUrl VARCHAR(255), "
#                                                         "workPackage_id INT, "
#                                                         "FOREIGN KEY (workPackage_id) REFERENCES workPackage(workPackage_id), "
#                                                         "stage_id INT, "
#                                                         "FOREIGN KEY (stage_id) REFERENCES stages(stage_id))")


# sql = "INSERT INTO company (RPM, name, address_line1, address_line2, address_line3, city, country, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# company = ("Yes", "RapidPM", "address_line1", "address_line2", "address_line3", "london", "uk", "00000")
# mycursor.execute(sql, company)
#
# mydb.commit()
#
# sql = "INSERT INTO customers (email, password, company_role, name, status, verified, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# customers = ("john@rpm.com", "admin", "Admin", "John", "Active", "Yes", "1")
# mycursor.execute(sql, customers)
#
# sql = "INSERT INTO projects (ProjectType, ProjectTitle, ProjectDescription, ProjectStart, ProjectEnd, customer_id, CustomerEmail) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# projects = [("Prince2", "rapidpm", "creation of a pm tool to rapidly project controls and oversight over projects", "3/14/2021", "5/28/2021", 1, "john@john.co.uk"),
#             ("Prince2", "myProject", "test project", "3/14/2021", "5/28/2021", 2, "musab@velastra.co.uk")]
# mycursor.executemany(sql, projects)
#
# sql = "INSERT INTO stages (StageName, StageDescription, Status, StageStart, StageEnd, project_id) VALUES (%s, %s, %s, %s, %s, %s)"
# stages = [("startup", "First phase of the project",	"Active", "3/14/2021", "4/3/2021", 1),
#             ("initiation", "Initialize project", "Active", "3/14/2021", "4/3/2021", 1),
#           ("startup", "First phase of the project", "Active", "3/14/2021", "4/3/2021", 2),
#           ("initiation", "Initialize project", "Active", "3/14/2021", "4/3/2021", 2)]
# mycursor.executemany(sql, stages)
#
# sql = "INSERT INTO workPackage (WorkPackageName, Description, Status, StartDate, EndDate, stage_id) VALUES (%s, %s, %s, %s, %s, %s)"
# workPackage = [("create customer management screen", "description",	"Active", "3/14/2021", "4/3/2021", 1),
#             ("customer mgt fixes", "description",	"Active", "3/14/2021", "4/3/2021", 1),
#                ("customer mgt fixes", "description",	"Active", "3/14/2021", "4/3/2021", 2),
#                ("customer mgt fixes", "description",	"Active", "3/14/2021", "4/3/2021", 3),
#                ("customer mgt fixes", "description",	"Active", "3/14/2021", "4/3/2021", 4)]
# mycursor.executemany(sql, workPackage)
#
# sql = "INSERT INTO artifacts (ArtefactName, ArtefactType, ArtefactProductType, ArtefactStatus, Manadatory, Multiples, DateCreated, TemplateUrl, LocationUrl, stage_id, workPackage_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# path = "/home/musab/RapidPM/RapidPM"
# arf = listdir(path)
#
# for a in arf:
#     artifact = (a, "PID", "Management", "Active", "Yes", "No", "4/3/2021", path+a, path+a, 1, 2)
#     mycursor.execute(sql, artifact)
# for a in arf:
#     artifact = (a, "PID", "Management", "Active", "Yes", "No", "4/3/2021", path+a, path+a, 2, 3)
#     mycursor.execute(sql, artifact)
# for a in arf:
#     artifact = (a, "PID", "Management", "Active", "Yes", "No", "4/3/2021", path+a, path+a, 4, 5)
#     mycursor.execute(sql, artifact)
#
mydb.commit()
#
# print(mycursor.rowcount, "record inserted.")

