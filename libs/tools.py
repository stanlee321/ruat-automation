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
        # image_captcha_link = get_image_link(response)
                
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
        prediction = predict("http://0.0.0.0:8000/predict", "captcha.png")
        
        # Else get the prediction
        #captcha = read_captha(prediction)
        captcha = input("Enter the captcha: ")
        payload = {
            "javax.faces.partial.ajax": True,
            "javax.faces.source": "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "busqueda",
            "busqueda:frmBusquedaVehiculo": "pnl-datosbusqueda:j_idt140: busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt140",
            "busqueda:frmBusquedaVehiculo": "busqueda:frmBusquedaVehiculo",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_focus:": "",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:criterio:ruatComboBox_input": "PTA",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:identificador-placapta:ruatInputText": "2787APK",
            "busqueda:frmBusquedaVehiculo:pnl-datosbusqueda:j_idt122:ruatCaptcha": captcha,
            "javax.faces.ViewState" : "841747812523742012:879031004355868399"
        }
        
        
        # Make post request to url
        api_url = "https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf?cid=4"
        response = session.post(api_url, data=payload)
        
        text = "El dato no coincide"
        
        if (text in response.text) or ("class javax.faces.applicat" in response.text):
            url = 'https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf'
            get_documents( url_base = url )
        else:
            with open('data.html', 'w') as f:
                f.write(response.text)
    

if __name__ == '__main__':
    
    url = 'https://www.ruat.gob.bo/vehiculos/consultageneral/InicioBusquedaVehiculo.jsf'
    
    get_documents( url_base = url )
    
    