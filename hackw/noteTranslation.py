# This class is used to summarize the notes of each slide
# Imports
import requests
import speech_recognition as sr
import cohere
import requests

# Global variables
api_key = "RG7HNjYkf3BPA7KkdWrb6VdqvVZXWNA78mNTwyvN"
co = cohere.Client(api_key)


# Convert speech to text
def speechToText(audio):
    # Initialize speech recognizer
    r = sr.Recognizer()

    # Load in the file
    filename = audio

    # Open the file and convert all recognized speech
    with sr.AudioFile(filename) as source:
        audioData = r.listen(source, 100, 100)
        return r.recognize_google(audioData)


# Punctuate text
def punctuate(text):

    endpoint = "http://bark.phon.ioc.ee/punctuator"

    # Call upon api
    response = requests.post(endpoint, params={
        "text": text
    })

    reply = response.content.decode()

    # Testing
    print(reply)
    print()
    print()

    # Close connection
    response.close()

    return reply

# Create a summary using cohere
def summary(audio):
    # Translate the audio to text
    text = speechToText(audio)

    # Punctuate data
    txt = punctuate(text)

    # Variables for processing
    bestText = " "
    bestSum = -1000

    # Leverage cohere to generate summary
    sumText = co.generate(
        model='command-xlarge-20221108',
        prompt=txt,
        return_likelihoods='GENERATION',
        temperature=0.8,
        max_tokens=120,
        num_generations=5
    )

    # Get the most likely text
    for gen in sumText:
        sumLikelihood = 0
        for t in gen.token_likelihoods:
            sumLikelihood += t.likelihood
        if bestSum < sumLikelihood:
            bestText = gen
            bestSum = sumLikelihood

    # Return summary
    return bestText

