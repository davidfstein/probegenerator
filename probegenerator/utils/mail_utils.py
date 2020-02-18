# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import base64
from argparse import ArgumentParser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)

def send_probes(recipient):
    message = Mail(
        from_email='davidmonlab@gmail.com',
        to_emails=recipient,
        subject='Your Probes Are Ready',
        html_content='Thank you for using probe generator. Your probes are attached.')
    with open('/data/results.zip', 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('application/zip')
    attachment.file_name = FileName('results.zip')
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('results')
    message.attachment = attachment
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

if __name__ == '__main__':
    userInput = ArgumentParser()
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-r', '--Recipient', action='store', required=True,
                                help='The recipients email.')
    args = userInput.parse_args()
    recipient = args.Recipient

    send_probes(recipient)