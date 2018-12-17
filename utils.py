import requests

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN="EAAFDHo95ZCuYBAHnp8nR91cFggZACnZAwfGyVXLNdOXQm4c4i3UzIfczo7s4P7UwWo78IpioGBXwvsKWXGZBZBrpiWitRoRR8zjZBSu0VZCQcIp2nMRiIrtUe4FxeKMfjm0ZBVdXEn1t7CeeqviWbwo3D21a4xRlLrgOum5tdsOATQZDZD"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response



def send_image_url(id, urls):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment":{
                "type": "image",
                "payload":{
                    #"is_reusable":"true"
                    "url": urls
                }
            }
        }
        #"filedata": "@/home/michael/Desktop/YBOTG/data/photo/20181216_181217_0001.jpg;type=image/jpg"
    }
    #filedata = "@/home/michael/Desktop/YBOTG/data/photo/20181216_181217_0001.jpg;type=image/jpg"
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    #pass
"""
def send_button_message(id, text, buttons):
    pass
"""
