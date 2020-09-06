from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as twilioClient
from twilio.http.http_client import TwilioHttpClient

from google.cloud import bigquery
from google.cloud import storage
from google.api_core.exceptions import InvalidArgument

import google.auth
import dialogflow

from urllib.parse import urlparse

import os
import threading
import time


# https://www.pythonanywhere.com/forums/topic/7021/ for this
proxy_client = TwilioHttpClient()
proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})

# Twilio authentication
account_sid = "twilio_sid"
auth_token = "twilio auth_token"
account_num = "twilio phone number you bought"

# Instantiates a Twilio client
twilio_client = twilioClient(account_sid, auth_token, http_client=proxy_client)

# GoogleCloud authentication for Dialogflow service account
path_to_key = '/home/<your-name-here>/mysite/secret-key.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_key

# Instantiates a Google Cloud storage client before doing anything else
google_cloud_storage_client = storage.Client()

# Dialogflow options
DIALOGFLOW_PROJECT_ID = 'google cloud project id'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
SESSION_ID = "anything you like, it doesn't matter"

# DialogFlow client
dialogflow_client = dialogflow.SessionsClient()
session = dialogflow_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

# BigQuery client needs to be authenticated with google auth
credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# Start Flask App
app = Flask(__name__)

# twilio connects to the webhook here when you text it
@app.route('/', methods=['GET', 'POST'])
def sms():
    # get the text message
    msg_from = request.values.get("From", None)
    msg_body = request.values.get("Body", None)
    
    # if you entered from the route then there was no message sent
    if not (msg_from and msg_body):
        return("Didn't work, did you get here directly?")

    # prepare inputs
    text_input = dialogflow.types.TextInput(text=msg_body, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    # dialogflow tries to understand what it is told
    try:
        response = dialogflow_client.detect_intent(session=session, query_input=query_input)
        dialogflow_answer = str(response.query_result.fulfillment_text)

    except InvalidArgument: # just in case
        raise

    if dialogflow_answer: # we use specific keywords to control the flow
        sending = ''
        
        if dialogflow_answer == '!why!':
            sending = 'Lipitor is used to treat high cholesterol levels. \
            High cholesterol blocks blood flow in blood vessels, \
            which increases the risk of strokes and heart attacks.'

        elif dialogflow_answer == '!prescriptions!':
            sending = 'Right now you are taking:\
            \n1. Truvada (HIV prevention)\
            \n2. Lipitor (high cholesterol treatment)'

        elif dialogflow_answer == '!side_effects!':
            sending = 'Lipitor can cause diarrhea, upset stomach, and muscle and joint pain.'

        elif dialogflow_answer == '!how_often!':
            sending = 'Your doctor has recommended that you take 1 pill per day.'

        elif dialogflow_answer == '!how_to_store!':
            sending = 'Store Lipitor in a closed container at room temperature. \
            Do not freeze. Keep away from heat, moisture, and direct light.'

        elif dialogflow_answer == '!when_to_take!':
            sending = 'Your doctor has recommended you take Lipitor in the evening.'

        elif dialogflow_answer == '!reminder!':
            sending = 'Got it! I’ll remind you to take 1 pill of Lipitor everyday at 6pm and 1 pill \
            of Truvada everyday at 9am!'

        else: # fallback
            sending = dialogflow_answer

        # send a text message back to patient
        twilio_client.messages.create(
            to = msg_from,
            from_ = account_num,
            body = sending)

        # demonstrating reminders
        if dialogflow_answer == '!reminder!':
            sending = 'It’s 6pm, please take 1 pill of Lipitor! (reminder {} of 3)'
            for i in range(3):
                time.sleep(4) # threads doesn't work on PythonAnywhere
                twilio_client.messages.create(
                to = msg_from,
                from_ = account_num,
                body = sending.format(i+1))
        return str(sending)

    else: # in case we visit the route directly

        return('Great, now try texting!')


# demonstrating dialogflow
@app.route('/dialogflowdemo', methods=['GET', 'POST'])
def hello():
    text_to_be_analyzed = "Hello"

    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = dialogflow_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    res = ''
    res = res + "Query text:" + str(response.query_result.query_text)
    res = res + "Detected intent:" + str(response.query_result.intent.display_name)
    res = res + "Detected intent confidence:" + str(response.query_result.intent_detection_confidence)
    res = res + "Fulfillment text:" + str(response.query_result.fulfillment_text)
    return(res)


# demonstrating bigquery with nlm_rx
# we were hoping to use this to generate text messages based on user input but we weren't able to get this to work
# because we don't know enough SQL
@app.route('/bigquerydemo', methods=['GET', 'POST'])
def bigquery():
    query = """
        SELECT
        *
        FROM
        `bigquery-public-data.nlm_rxnorm.rxnconso_current`
        WHERE
        rxcui =  '5640'
        """
    # find all entries with ibuprofen
    df = bigquery_client.query(query).to_dataframe()  # Make a BigQuery and convert to Pandas Dataframe

    return df.to_string()
