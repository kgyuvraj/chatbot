from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pywhatkit as pwt
import pyjokes
from helpdoc import help_text,autoResponse
import random

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter", logic_adapters=[
    {
        'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        'input_text': 'empty',
        'output_text': ''
    },
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'i honestly have no idea how to respond to that',
        'maximum_similarity_threshold': 0.9
    },
    {
        'import_path': 'chatterbot.logic.MathematicalEvaluation'
    }

])


# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")
# trainer.train("chatterbot.corpus.hindi")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userTextLower = userText.lower()
    # using pywhatkit for wikipedia search
    if userTextLower.startswith("wiki"):
        pwt_response = pwt.info(userText[5:], return_value=True, lines=2)
        return pwt_response
    # using pywhatkit for image to ascii art generator
    elif userText.startswith("img to ascii"):
        pwt_response = pwt.image_to_ascii_art(userText[13:], "ascii")
        print(pwt_response)
        f = open('ascii.txt', 'r')
        file_contents = f.read()
        return file_contents
        f.close()
        # using pywhatkit for google search
    elif userTextLower.startswith("google"):
        pwt_response = pwt.search(userText[7:])
        return "Here's what i found on google..."
        return pwt_response
    # using pywhatkit for playing videos on youtube
    elif userTextLower.startswith("youtube"):
        userText = userText.lower()
        return "playing.."
        pwt.playonyt(userText[8:], use_api=True)
    # using pyjokes to listen a joke
    elif userTextLower.startswith("tell me a joke") or userText.startswith("tell me joke") or userText.startswith(
            "joke"):
        return pyjokes.get_joke()
    # for assistance helpdesk
    elif userTextLower.__contains__("help"):
        return help_text
    #    elif userText.startswith("sendmsg "):
    #  try:
    # sending message to receiver
    # using pywhatkit
    # pwt_msg=pwt.sendwhatmsg("+919936303919",
    #         userText[8:],
    #        13, 37)
    # return (pwt_msg)
    # print("Successfully Sent!")

    # except:
    # handling exception
    # and printing error message
    # print("An Unexpected Error!")
    # using chatterbot for any random response
    else:
        return random.choice(autoResponse)


if __name__ == "__main__":
    app.run()
