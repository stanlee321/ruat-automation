import random
from bs4 import BeautifulSoup
import uuid
import requests
import json
import base64
import time
from typing import Any


def predict(url:str, image_path:str ) :
    """
        This function predicts the captcha from the image_path and returns the captcha.
    """
    print("predicting with...", url)
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read())

    # Setup separate json data
    payload = {
        "mime" : "image/png",
        "img_bytes": base64_image,
    }

    response = requests.post(url, data = payload)
    
    return json.loads(response.text)


def read_captha(res):
    '''

    '''
    
    data = json.loads(res['data'])
    captcha = ''
    
    for d in data["predictions"]:
        captcha += d['text']
    return captcha.replace(' ', '').upper()





def get_image_link(response) -> str:
    """
        This function returns the image link from the response.
    """
    soup = BeautifulSoup(response.text, 'html')

    images = soup.find_all("img")
        
    for image in images:
        src = image.attrs.get("src")
        if '/Captcha.png?' in src:
            return src


def get_payload_3(file):

    with open(file, 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        
    inputs = soup.find_all("input")
    payload = {}
    for input in inputs:
        # print(input)
        input_value = input.attrs.get("value")
        input_id= input.attrs.get("id")
        
        if input_id is not None:
            payload[input_id] = input_value
    return payload




def get_captcha_link():
    """
        function actualizarCaptcha(){
        document.getElementById("40132659").src="/Captcha.png?" + (Math.random()+"").substring(2, 7);
    }
    $("input[id*='ruatCaptcha']").val("");
    """
    # The Python equivalent to (Math.random()+"").substring(2, 7);
    random_num = str(random.random())[2:7]
    
    return "/Captcha.png?" + random_num

def get_post_data(response) ->  dict:
    """
        This function returns the image link from the response.
    """
    soup = BeautifulSoup(response.text, 'lxml')

    form = soup.find("form", {"id": "busqueda:frmResultadoBusqueda"})
    src = form.attrs.get("action")

    state_raw = soup.find("input",  {"id": "j_id1:javax.faces.ViewState:1"})
    state = state_raw.attrs.get("value")
    return {"src": src, "state": state}

        
        
        
def get_documents( url_base:str )  -> Any:
    """
        This function returns the documents from the impuestos.gob.bo website.
    """
    
    with requests.session() as session:

        # Make First Request
        
        print('Making first request...')
        print(url_base)
        try:
            response = session.get(url_base)
        except Exception as e:
            print(e)
            print(f"cannot reach url: {url_base}")
            return None
        
        # Save Captcha
        post_data = get_post_data(response)
        # print(post_data["src"].split("?")[-1])
        # print("Link", post_data)
        
        image_captcha_link = get_captcha_link()
        
        # Image Captcha placeholde        
        if image_captcha_link:
            captcha_link = "https://www.ruat.gob.bo/" + image_captcha_link

            print("Dowlnoading captcha image")

            # Download image as PNG called captcha.png
            res = session.get( captcha_link )
            with open('captcha.png', 'wb') as f:
                # save image
                f.write(res.content)

        # Request input from user into the variable captcha
        captcha = ''
        
        # if False:
        #     # Manual input
        #     captcha = input("Enter the captcha: ")
        # else :
        
        # Predict captcha using API
        # prediction = predict("http://0.0.0.0:8000/predict", "captcha.png")
        
        # Else get the prediction
        #captcha = read_captha(prediction)
        
        captcha = input("Enter the captcha: ")
        
        payload = {
            "busqueda:frmBusquedaVehiculo": "busqueda:frmBusquedaVehiculo",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_focus": "",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_input": "PTA",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:identificador-placapta:ruatInputText":"2787APK",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt122:ruatCaptcha": captcha,
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140": "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
            "javax.faces.ViewState": post_data["state"],
            "javax.faces.partial.ajax": "true",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "busqueda",
            "javax.faces.source": "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
        }
        print("payload", payload)
        
        state = post_data["state"]
        data = f"javax.faces.partial.ajax=true&javax.faces.source=busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Aj_idt140&javax.faces.partial.execute=%40all&javax.faces.partial.render=busqueda&busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Aj_idt140=busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Aj_idt140&busqueda%3AfrmBusquedaVehiculo=busqueda%3AfrmBusquedaVehiculo&busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Acriterio%3AruatComboBox_focus=&busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Acriterio%3AruatComboBox_input=PTA&busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Aidentificador-placapta%3AruatInputText=2787APK&busqueda%3AfrmBusquedaVehiculo%3Apnl-datosbusqueda%3Aj_idt122%3AruatCaptcha={captcha}javax.faces.ViewState={state}"
        print
        print(data)
        xml = f"""<?xml version='1.0' encoding='utf-8'?>
        {data}"""
        #print(payload)
        api_base_url = "https://www.ruat.gob.bo"
        # Make post request to url
        # api_url = "/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf?cid=4"
        api_url = api_base_url + "/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf?" + post_data["src"].split("?")[-1]
        print("posting to ...", api_url)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded', # set what your server accepts
            "Host": "www.ruat.gob.bo",
            "Origin": "https://www.ruat.gob.bo",
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding" : "gzip, deflate, br",
            "Referer": "https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf"
        }


        response = session.post(api_url,
                                data=payload,
                                headers=headers)
        print(response.status_code)
        
        history = response.history
        
        print("history", history)
        print("redirected to", response.url)
        
        with open('data.html', 'w') as f:
            f.write(response.text)
            
        cook = session.cookies.get_dict()["JSESSIONID"]
        
        print(session.cookies.get_dict())
        
        print(cook)
        res2 = session.get("https://www.ruat.gob.bo/vehiculos/consultageneral/ConsultaDeuda.jsf?cid=1",
                           headers= {
                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                               "initiator": "https://www.ruat.gob.bo",
                                "Referer": "https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf",
                            },
                           cookies={
                                "JSESSIONID": cook
                           },
                           )
        print(res2.status_code)
        
        history = res2.history
        
        for h in history:
            print(",,,",h.url)
        
        
        print("history", history)
        print("redirected to", res2.url)
        
        with open('data2.html', 'w') as f:
            f.write(res2.text)
            
        res3 = session.get( res2.url,
                                headers= {
                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                               "initiator": "https://www.ruat.gob.bo",
                                "Referer": "https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf",
                            },
                           cookies={
                                "JSESSIONID": cook
                           }
                           )
        
        with open('data3.html', 'w') as f:
            f.write(res3.text)
            
            
        post_data_3 = get_post_data(res3)
        

        payload_3 = {
            "busqueda:frmBusquedaVehiculo": "busqueda:frmBusquedaVehiculo",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_focus": "",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_input": "PTA",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:identificador-placapta:ruatInputText":"2787APK",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140": "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
            "javax.faces.ViewState": post_data_3["state"],
            "javax.faces.partial.ajax": "true",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "busqueda",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt122:ruatCaptcha": "",
            "javax.faces.source": "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
        }
        
        api_url = "https://www.ruat.gob.bo/vehiculos/consultageneral/ConsultaDeuda.jsf?cid=1"


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded', # set what your server accepts
            "Host": "www.ruat.gob.bo",
            "Origin": "https://www.ruat.gob.bo",
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding" : "gzip, deflate, br",
            "Referer":  "https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf"
        }


        response = session.post(api_url,
                                data=payload_3,
                                headers=headers,
                                cookies={
                                    "JSESSIONID": cook
                                }
                                )
        print(response.history)
        for h in response.history:
            print(",,,",h.url)
        with open('data4.html', 'w') as f:
            f.write(response.text)
        # if (text in response.text) or ("class javax.faces.applicat" in response.text):
        #     url = 'https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf'
        #     get_documents( url_base = url )
        # else:
        #     with open('data.html', 'w') as f:
        #         f.write(response.text)
    

if __name__ == '__main__':
    
    url = 'https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf'
    
    get_documents( url_base = url )
    
    