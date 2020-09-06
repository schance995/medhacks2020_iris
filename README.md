# We are Team Empowerment Through Information at MedHacks2020, and this is 
![Iris Logo](Iris.png)


## Pitch 
Iris is an SMS chatbot that provides patients with information about the medications they are taking, such as side effects, how often they should be taken, and active ingredients.
 
## Our Story
According to the WHO, an estimated 125,000 people die from medication nonadherence per year. These deaths are entirely preventable, and two of their main causes are patients lacking belief in their need for medication and having fear of a medication’s possible side effects. On top of this, forgetting to take a dose of their medication accounts for 39% of all patient nonadherence. If patients can conveniently access easy-to-digest information about their prescriptions, they will be more likely to take their medications. Beyond being informed, patients will greatly benefit from critical medication reminders to further increase patient adherence. 

This is where Iris comes in.

Iris is an SMS chatbot that patients can text to gain easily understandable information about the medications they are taking. With the patient’s permission, the physician will submit information about the patient’s prescriptions to our server. After the patient leaves, the patient can text Iris with any questions about the prescribed medications. The information Iris will provide includes the total medications that were prescribed, each medication’s active ingredient, the purpose of each medication, and the potential side effects. The doctor can also choose to provide additional patient-specific information, such as information on dosage and when the medication should be taken. If such supplementary information is provided, the patient can opt for reminder texts to be sent when it is time for the patient to take their medications. 

The choice of using an SMS-bot stems from the need to make such information much more accessible than it is now, especially to those lacking literacy in technology. All a patient needs to do get started is to set up the initial account at their physician’s office then start texting - there’s no need for the patient to install anything or create any additional accounts.

With Iris, we hope to educate patients about the drugs they have been prescribed. If patients feel that they understand why they are taking certain medications and how exactly to take them, they will be more motivated to adhere to physician-prescribed treatment plans. Iris aims to empower patients in learning about their healthcare needs.  

You can text Iris at 1-202-935-7045. Iris will be available to chat until after MedHacks closes.

## [Check out our presentation slides](https://docs.google.com/presentation/d/e/2PACX-1vRKhjLxvHEs-NEv6R-ggEIgcV1AvITJMRmlhUY5z-mSYtYSZ9VuUJN4dPbZ3hc2PxXhEGi_-opqxuQw/pub?start=false&loop=false&delayms=3000)
## [And our demo video](https://drive.google.com/file/d/1kTpveKhr2RIRTMteFti6UtP7KMVuElOH/view?usp=sharing) 

## Works Cited
Allison, K. (2012). Adherence through education: A call to clinicians to educate all patients on medication use. Mental Health Clinician, 2(4), 83–85. <https://doi.org/10.9740/mhc.n117761>

Brown, M. T., & Bussell, J. K. (2011). Medication Adherence: WHO Cares? Mayo Clinic Proceedings, 86(4), 304–314. <https://doi.org/10.4065/mcp.2010.0575>

Martin, L. R., Williams, S. L., Haskard, K. B., & DiMatteo, M. R. (2005). The challenge of patient adherence. Therapeutics and Clinical Risk Management, 1(3), 189–199.

McCarthy, R. (1998). The price you pay for the drug not taken. Business and Health, 16(10), 27–28, 30, 32–33.



# Building Iris
The steps are similar to [this tutorial](https://chatbotslife.com/build-a-working-sms-chat-bot-in-10-minutes-b8278d80cc7a) but have to be modified to match [this tutorial](https://medium.com/swlh/working-with-dialogflow-using-python-client-cb2196d579a4) because many updates have happened since. It helps if you know Python and Flask so you can debug if things go wrong, but ideally if you carefully follow these steps everything should work out.

## Here We Go
0. Read the docs for setting up [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/setup)
1. Create a DialogFlow service account on Google Cloud
1. Check that the billing of the service account is set to the trial account.
2. In DialogFlow create an agent based off the FAQ template (we had to create a new agent first to enable making off of templates)
3. Create different intents that respond to different queries. Each intent should return a message formatted `!message!`. This unique format was arbitrarily chosen to avoid confusing it with DialogFlow's more natural responses.
    - For example, you can modify the `welcome` intent to return `Hi, my name is Iris!` when the patient texts `Hello`.
    - Our code has examples of handling these outputs
    - In theory, DialogFlow matches texts with their intents, and from those intents we can use BigQuery on the [nlm-rxnorm dataset](https://www.nlm.nih.gov/research/umls/rxnorm/overview.html) (also available on Google Cloud). But we weren't able to figure this out in time for the weekend :(
    - Maybe you know how to work with this, if so our code has BigQuery set up so you can make queries! :)
3. Instead of a client access token you will need a JSON key file. Follow the docs [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=en).
4. Download this JSON key file and keep it safe since, it's your private information!
4. Make a [Twilio](https://www.twilio.com/) account.
4. Buy a cellphone number with SMS only, it costs $1 but you should have a free trial so you can afford it.
4. Note your Twilio identify information (authentication, etc).
4. Create a new WebApp on [PythonAnywhere](https://www.pythonanywhere.com/)
5. Select 'Flask' for Python 3.6 (we weren't sure if higher versions would break the libraries)
6. Load **flask_app.py** into PythonAnywhere. You will need to replace the private account details in the areas listed in the file.
     - If you choose to experiment with BigQuery you will need to grant BigQuery Admin access to your service account. If we remember correctly, DialogFlow agents should already have permission to use DialogFlow. You can simply grant the same DialogAgent the BigQuery access role.
7. Also load up **requirements.txt** and your GoogleCloud JSON key into the online filesystem.
8. Go to bash in PythonAnywhere, and create a [virtual environment](https://help.pythonanywhere.com/pages/Virtualenvs/)
    - Use Python 3.6 to match the Flask version. We used a virtual environment because some of the libraries broke without it.
8. Activate the virtual environment
9. In bash: `pip install -r requirements.txt` for the required libraries
10. Start the web app. You can test it by going to the other routes besides the root page, this will return text of some simple DialogFlow and BigQuery usage.
10. Go back to your Twilio account, and in "Manage numbers" set the webhook to your web app's link. You only need the landing (home) page for this unless you changed the route name in Flask.
10. This is it! Text the phone number you bought from Twilio!
    - If Iris responded then you've successfully completed this tutorial!
    - Otherwise please see the next section.

## Debugging
Here are some common errors we ran across:
- Check that you are importing the correct, **not deprecated** libraries. Many of Google's libraries in particular seem to stale quickly, so whatever docs you read on Google Cloud might be out of date.
- Make sure that you have entered all your authentication information correctly.
- Make sure that your Google Cloud project is properly set up (billing, service accounts/permissions, etc)
- Make sure you reload PythonAnywhere after making any changes (this one really got us for a while)

## Thanks for your interest in Iris!
- Spencer Chan
- Tanaya Jha
- Michelle Fang
- Surya Padmanabhan
