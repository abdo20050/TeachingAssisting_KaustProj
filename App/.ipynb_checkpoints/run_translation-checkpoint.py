#microsoft Translation API
import requests, uuid, json

def respons_to_text(response):
    text = response[0]['translations'][0]["text"]
    return text

def translate_text(input:str):

    key = "ed5ba8194627441faf60396db9ea00a7"
    endpoint = "https://api.cognitive.microsofttranslator.com/"


    location = "uaenorth"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',

        'to': ['ar']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }


    body = [{
        'text': input
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    output = respons_to_text(response)
    return output