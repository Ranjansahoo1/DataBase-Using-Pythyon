import pandas as pd
import smtplib
import psf_src_9500_PremTrxStg_InsPro_main as parmext
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import configparser as conf
import os.path
from datetime import datetime

jobruntime = datetime.now().strftime("%Y%m%d%H%M%S")
jobrundate = datetime.today().strftime('%Y-%m-%d')

def get_config(configure_path):
    config = conf.ConfigParser()
    # read config file
    config.read(configure_path)
    premb_params = config['premium']
    return premb_params


# Common function to send email notification
def fn_send_email(sendfrom, sendto, filename, subject, text):
    try:
        msg = MIMEMultipart()
        msg['From'] = sendfrom
        msg['To'] = ", ".join(repr(email) for email in sendto)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if filename != '':
            with open(filename, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(filename)
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
            msg.attach(part)

        smtp = smtplib.SMTP('mail.pmic.com')
        smtp.sendmail(sendfrom, sendto, msg.as_string())
        smtp.close()
        code = 0
    except Exception as error:
        code = 1
        print('psf_src_9900_PremTrxStg_InsPro_email_not : send email error ' + str(error) + '\n')
    return code

# Function to assign the To email, From Email, Subject, Text and Conditions to send email
# For premium transactions where adjustments were made, we send those records if they exist
def fn_send_prem_adjust_notification(config_path, logger):
    try:
        # Read config and secret
        # config_path = "/home/pmic-py/properties.ini"
        config = conf.ConfigParser()
        config.read(config_path)
        email_params = config['premium']

        # Setting up from email, To email, text and subject for policies with premiums adjusted
        prm_environment = email_params['prm_environment']
        sendfrom = email_params['sendfrom']
        sendto = email_params['sendto']

        notification_file = parmext.output_path + 'prem_trans_adjusted_rates_policies.txt'
        file_exists = os.path.exists(notification_file)
        subject = prm_environment + '   -  Adjusted premiums by few cents'
        text = 'Attached file contains list of policies where premiums were adjusted by few cents.\n  ' \
               '' \
               '' \
               '\n' \
               '\n' \
               'Thanks,\n' \
               'ETL Support'

        if file_exists:
            notification_data = pd.read_csv(notification_file)
            if len(notification_data) > 0:
                fn_send_email(sendfrom, sendto, notification_file, subject, text)
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_adjust_notification : has records to be sent '
                            'to Business')
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_adjust_notification : '
                            'call function fn_send_email complete')
                code = 0
            else:
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_adjust_notification : There are no policies '
                            'with premiums adjusted')
                code = 0
        else:
            logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_adjust_notification : '
                        'prem_trans_adjusted_rates_policies.txt does not exist')
            code = 0

    except Exception as error:
        print('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_adjust_notification : Issue in sending file '
              + str(error) + '\n')
        code = 1
    return code

# Function to assign the To email, From Email, Subject, Text and Conditions to send email
# For premium transactions where date adjustments were made, we send the records if they exist
def fn_send_prem_dates_adjust_notification(config_path, logger):
    try:
        # Read config and secret
        # config_path = "/home/pmic-py/properties.ini"
        config = conf.ConfigParser()
        config.read(config_path)
        email_params = config['premium']

        # Setting up from email, To email, text and subject for policies with premiums adjusted
        prm_environment = email_params['prm_environment']
        sendfrom = email_params['sendfrom']
        sendto = email_params['sendto']

        notification_file = parmext.output_path + 'psf_src_9600_prem_trans_fn_prem_trans_default_dt_file.txt'
        file_exists = os.path.exists(notification_file)
        subject = prm_environment + '   -  Premiums had Nulls in few date columns'
        text = 'Attached file contains list of policies where dates for premiums were adjusted as they were NULL.\n  ' \
               '' \
               '' \
               '\n' \
               '\n' \
               'Thanks,\n' \
               'ETL Support'

        if file_exists:
            notification_data = pd.read_csv(notification_file)
            if len(notification_data) > 0:
                fn_send_email(sendfrom, sendto, notification_file, subject, text)
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_dates_adjust_notification : has records to be sent '
                            'to Business')
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_dates_adjust_notification : '
                            'call function fn_send_email complete')
                code = 0
            else:
                logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_dates_adjust_notification : There are no policies '
                            'with dates in premiums adjusted')
                code = 0
        else:
            logger.info('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_dates_adjust_notification : '
                        'psf_src_9600_prem_trans_fn_prem_trans_default_dt_file.txt does not exist')
            code = 0

    except Exception as error:
        print('psf_src_9900_PremTrxStg_InsPro_email_not.fn_send_prem_dates_adjust_notification : Issue in sending file '
              + str(error) + '\n')
        code = 1
    return code
