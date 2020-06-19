import os
import sys 
from s3_utils import main
from argparse import ArgumentParser
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_probes(recipient, url, retry_count=0):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Monaghan Lab <davidmonlab@gmail.com>"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = recipient

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Your Probes Are Ready"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "Thank you for using probe generator. Your probes can be downloaded here: " + url + \
        "Your results will be available for download for 24 hours, after which they will removed."

    # The HTML body of the email.
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <h1>Monaghan Lab - Probe Generator</h1>
    <p>Thank you for using probe generator. Your probes can be downloaded here: """ + \
    url + """</p>
    <p>Your results will be available for download for 24 hours, after which they will removed. </p>
    </body>
    </html>
    """

    # The character encoding for the email.
    CHARSET = "utf-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            # ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        if (retry_count < 5):
            send_probes(recipient, url, retry_count+1)
            print(e.response['Error']['Message'])
        else:
            sys.exit(1)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

if __name__ == '__main__':
    userInput = ArgumentParser()
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-r', '--Recipient', action='store', required=True,
                                help='The recipients email.')
    requiredNamed.add_argument('-j', '--Job', action='store', required=True,
                                help='The recipients email.')
    args = userInput.parse_args()
    recipient = args.Recipient
    job_id = args.Job

    url = main("/data/results.zip", "probegenerator-results", job_id)

    send_probes(recipient, url)