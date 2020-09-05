from flask import Flask, request
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as twilioClient

from urllib.parse import urlparse

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

proxy_client = TwilioHttpClient()
proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

# https://www.pythonanywhere.com/forums/topic/7021/

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/your-name-here/mysite/secret-key.json'

account_sid = "twilio_sid"
auth_token = "twilio auth_token"
account_num = "twilio account_number"

DIALOGFLOW_PROJECT_ID = 'project_id'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = 'anything'

# https://cloud.google.com/storage/docs/reference/libraries
# no need to create buckets
# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
client = twilioClient(account_sid, auth_token, http_client=proxy_client)

#client = twilioClient(account_sid, auth_token)
storage_client = storage.Client()

# start flask app
app = Flask(__name__)

# start dialogflow
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

# twilio sends requests here
@app.route('/', methods=['GET', 'POST'])
def sms():
    msg_from = request.values.get("From", None)
    msg_body = request.values.get("Body", None)

    text_input = dialogflow.types.TextInput(text=msg_body, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    # pass text to dialogflow and get a response
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        chatbot_answer = str(response.query_result.fulfillment_text)

    except InvalidArgument:
        raise

    if chatbot_answer: # send it
        client.messages.create(
            to = msg_from,
            from_ = account_num,
            body = chatbot_answer)
        return str(chatbot_answer)
    else:
        return 'Great, now try texting!'
    return 'a' + str(msg_from) + str(msg)

@app.route('/hello', methods=['GET', 'POST']) # test
def hello():
    text_to_be_analyzed = "Howdy"

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    res = ''
    res = res + "Query text:" + str(response.query_result.query_text)
    res = res + "Detected intent:" + str(response.query_result.intent.display_name)
    res = res + "Detected intent confidence:" + str(response.query_result.intent_detection_confidence)
    res = res + "Fulfillment text:" + str(response.query_result.fulfillment_text)
    return(res)
