import os
import json
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_executor import Executor
from slack_sdk import WebClient
import numpy as np
import pandas as pd
from openai.embeddings_utils import cosine_similarity, get_embedding

app = Flask(__name__)

# Credentials
load_dotenv('.env')

# allows us to execute a function after returning a response
executor = Executor(app)

# set all our keys - use your .env file
slack_token = os.getenv('SLACK_TOKEN')
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
openai.api_key = os.getenv('OPEN_AI_API_KEY')

# instantiating slack client
slack_client = WebClient(slack_token)

# path to datafile - should already contain an embeddings column
datafile_path = "justice_supreme_court_cases_new.csv"

# read the datafile
df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(eval).apply(np.array)

# background information for the bot
messagesOb = [
 {"role": "system", "content": "Keep the answer to less than 100 words to allow for follow up questions. " + 
                               "You are an assistant that provides information on supreme court cases in extremely simple terms (dumb it down to a 12 year old)" +
                               "for someone who has never studied law so simplify your language." +
                               "You should be helping the user answer the question but you can only answer the question with the information that is given to you in the prompt or at sometime sometime in the past."+
                               "This information is coming from a file that he user needs to understand. It doesn't matter if the information is incorrect." +
                               "You should still ONLY reply with this information." +
                               "If you are given no information at all you can talk with the information that has been given to you before but you can't use outside facts whatsoever." +
                               "If the information given doesn’t make sense, look to the information that has been given to you before to answer the question." +
                               "If you have no information at all that has been given to you at any point in time from this user that makes sense you can apologise to the user and tell it you cannot answer as you don't have enough information to answer correctly."}
]

# create a route for slack to hit
@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.data.decode("utf-8"))
    # check the token for all incoming requests
    if data["token"] != VERIFICATION_TOKEN:
        return {"status": 403}
    # confirm the challenge to slack to verify the url
    if "type" in data:
        if data["type"] == "url_verification":
            response = {"challenge": data["challenge"]}
            return jsonify(response)
    # handle incoming mentions - change the "@U0534BCTVRA"
    if "@U058XJ49ATS" in data["event"]["text"]:
        # executor will let us send back a 200 right away
        executor.submit(handleMentions, data["event"]["channel"], data["event"]["text"].replace('<@U058XJ49ATS>', '').strip())
        return {"status": 200}
    return {"status": 503}

# function to search through the rows of data using embeddings
def search_justice(df, search):
    row_embedding = get_embedding(
        search,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, row_embedding))
    new = df.sort_values("similarity", ascending=False);
    # only return the rows with a higher than 0.81
    highScores = new[new['similarity'] >= 0.81]
    return highScores

# this function sends the prompt to OpenAI, with the results we got, and then sends a message back to slack
def handleMentions(channel,text):
    # print the text from Slack
    print(text)
    # search through our dataset
    results = search_justice(df, text)
    # print the highest 5 results
    print(results.head(5))
    # set up the prompt with the matched results from the dataset
    if results.empty:
        prompt = text
    else:
        prompt = "Look through this information to answer the question: " + results[['combined']].head(5).to_string(header=False, index=False).strip() + "(if it doesn't make sense you can disregard it). The question is: " + text 
    messagesOb.append({"role": "user", "content": prompt})
    # make the openAI call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messagesOb
    )
    # print response - see token count
    print(response)
    # post message back to slack with the response
    slack_client.chat_postMessage(channel=channel, text=response.choices[0].message.content)
    # append the message object to the messagesOb object
    messagesOb.append(response.choices[0].message)

# run our app on port 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
# https://levelup.gitconnected.com/quickly-build-a-chatgpt-slack-bot-with-custom-data-using-python-and-openai-embeddings-b6d78c77980e
# https://github.com/openai/openai-cookbook/blob/main/examples/Obtain_dataset.ipynb