import smtplib, ssl

# port = 465  # For SSL
# password = input("Type your password and press enter: ")
# 
# # Create a secure SSL context
# context = ssl.create_default_context()
# 
# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("rapidpm.musab@gmail.com", password)
#     server.sendmail("rapidpm.musab@gmail.com", "muhammadmusab92@gmail.com", "hi")
def sendEmail():
  msg = "hi"
  port = 465
  password="@Mushi123"
  # Create a secure SSL context
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("rapidpm.musab@gmail.com", password)
    server.sendmail("rapidpm.musab@gmail.com", "muhammadmusab92@gmail.com", msg)