# Iris: MedHacks2020, Team Empowerment Through Information

## Pitch 
Iris is an SMS chatbot that provides patients with information about the medications they are taking, such as side effects, how often they should be taken, and active ingredients.

 
## Our story
According to the WHO, an estimated 125,000 people die from medication nonadherence per year. These deaths are entirely preventable, and two of their main causes are patients lacking belief in their need for medication and having fear of a medication’s possible side effects. On top of this, forgetting to take a dose of their medication accounts for 39% of all patient nonadherence. If patients can conveniently access easy-to-digest information about their prescriptions, they will be more likely to take their medications. Beyond being informed, patients will greatly benefit from critical medication reminders to further increase patient adherence. 

This is where Iris comes in.

Iris is an SMS chatbot that patients can text to gain easily understandable information about the medications they are taking. With the patient’s permission, the physician will submit information about the patient’s prescriptions to our server. After the patient leaves, the patient can text Iris with any questions about the prescribed medications. The information Iris will provide includes the total medications that were prescribed, each medication’s active ingredient, the purpose of each medication, and the potential side effects. The doctor can also choose to provide additional patient-specific information, such as information on dosage and when the medication should be taken. If such supplementary information is provided, the patient can opt for reminder texts to be sent when it is time for the patient to take their medications. 

The choice of using an SMS-bot stems from the need to make such information much more accessible than it is now, especially to those lacking literacy in technology. All a patient needs to do get started is to set up the initial account at their physician’s office then start texting - there’s no need for the patient to install anything or create any additional accounts.

With Iris, we hope to educate patients about the drugs they have been prescribed. If patients feel that they understand why they are taking certain medications and how exactly to take them, they will be more motivated to adhere to physician-prescribed treatment plans. Iris aims to empower patients in learning about their healthcare needs.  


## [Check out our presentation slides](https://docs.google.com/presentation/d/1NEmPzCgbp9Jrm1FA_ZTljlaCUCwe93AI_pcHt4aa2z0/edit?ts=5f540474#slide=id.g970400d85f_1_18367)
## [And our demo video](https://drive.google.com/file/d/1kTpveKhr2RIRTMteFti6UtP7KMVuElOH/view?usp=sharing) 


# GETTING THE TUTORIAL TO WORK
The steps are similar to [this](https://chatbotslife.com/build-a-working-sms-chat-bot-in-10-minutes-b8278d80cc7a) but have to be modified to match [this](https://medium.com/swlh/working-with-dialogflow-using-python-client-cb2196d579a4) because times have changed (api.ai is now DialogFlow for starters).

## SETUP
0. Read the docs for setting up [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/setup)
1. Claim your Google Cloud credits first.
1. Create a DialogFlow service account on Google Cloud
1. Check that the billing of the service account is set to the trial account (this gave me a headache).
2. In DialogFlow create an agent (you need to create a new agent before picking a template like FAQ)
3. Instead of a client access token you will need a private key file. Read the docs for this one.
4. Make a [Twilio](https://www.twilio.com/) account.
4. Buy a cellphone number, it costs $1 but you should have a free trial so you can afford it.
4. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
5. Add a new WebApp, select 'Flask' for Python 3.6
6. Load flask_app.py into the web app. You will need to replace the account details in the areas listed in the file. This may take some time to find everything.
7. Also load up requirements.txt and your private key into the online filesystem.
8. Go to bash in PythonAnywhere, and create a virtual environment for 3.6.
8. Switch into the virtual environment
9. `pip install -r requirements.txt` for the required packages
10. Text the phone number you bought and hope it works!

## Get ready to code
1. [Download Git](https://git-scm.com/downloads)
2. Go to your Documents folder or your favorite file location
3. Using git bash: `git clone https://github.com/schance995/medhacks2020.git`

## Now you're ready
You can also do this with git GUI but I can't help you as much with that.
1. Write code, make changes, have fun!
2. `git add .` to stage your changes
  - if you did this too early it's fine: `git reset` to unstage changes
3. `git commit -m "describe your changes here"` to save your changes to the log
4. `git push origin master` to update them to the master repository

## Notes
- git is decentralized version control, so when one person makes an update everyone has to download the update using `git pull`
- I don't expect us to learn how to pull and fork in one day (the proper way to work on a collaborative git project). This is a small project so it doesn't matter but let's try to avoid working on too many parts of the code at once so we can reduce the chances of errors of code mismatching (these are a pain to fix)
- Please check the google doc for more information aobut our project.
