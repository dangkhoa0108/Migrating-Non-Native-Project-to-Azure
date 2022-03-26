from email import message
import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    connection = psycopg2.connect(user = "pgadmin@khoadpgserver",
                                  password = "Zxcvb@12",
                                  host = "khoadpgserver.postgres.database.azure.com",
                                  port = "5432",
                                  database = "techconfdb")
    cursor = connection.cursor()

    try:
        noti_query = '''SELECT subject, message from Notification where id = %s;'''
        cursor.execute(noti_query, (notification_id,))
        notification = cursor.fetchone()
        sj = notification[0]
        body = notification[1]

        attendees_query = '''select first_name, email from Attendee;'''
        cursor.execute(attendees_query)
        attendees = cursor.fetchall()
        for attendee in attendees:
            first_name = attendee[0]
            email = attendee[1]
            c_subject = f'Xin chao, {first_name}: {sj}'
            send_email(email= email, subject= c_subject, body=body)

        date = datetime.utcnow()
        status = f'{ len(attendees) } Tech Conf 2022 attendees notified.'
        update_query = '''UPDATE Notification 
                                SET completed_date = %s, status = %s 
                                WHERE id = %s;'''
        cursor.execute(update_query, (date, status, notification_id))
        connection.commit()
        count = cursor.rowcount
        logging.info(f"{ count } records successfully updated.")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if(connection):
            cursor.close()
            connection.close()

def send_email(email, subject, body):
    message = Mail(
        from_email="tdangkhoa.itute@gmail.com@gmail.com",
        to_emails=email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient("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")
        sg.send(message)
    except Exception as e:
        logging.info("Unable to send message using SendGrid API.")