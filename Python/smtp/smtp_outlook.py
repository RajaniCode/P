import smtplib

# Connect to the smtp server
server = smtplib.SMTP('smtp.live.com', '587')

# Start TLS encryption
server.starttls()

# Login
from_email = "*****@outlook.com"
password = "********"
server.login(from_email, password)
to_email = "#####@gmail.com"

# Send email 
message = "Subject: Email using Python\n"
message += "Email using Python Hello World!"    
server.sendmail(from_email, to_email, message)
server.quit()
