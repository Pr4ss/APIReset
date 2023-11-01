import requests
import hashlib
import secrets
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class APIReset(App):
    def build(self):
        return myGrid()

class myGrid(BoxLayout):
    def __init__(self, **kwargs):
        super(myGrid, self).__init__(**kwargs)
        self.requisicao_em_andamento = False

        self.image = self.ids.my_image
        self.responseMsg = self.ids.response_msg
        self.inputIP = self.ids.input_ip
        self.inputSenha = self.ids.input_senha
        self.resetButton = self.ids.reset_button

    
    def desabilitar_botao(self):
        button = self.ids.reset_button
        button.disabled = True  
        Clock.schedule_once(self.reabilitar_botao, 5)  

    def reabilitar_botao(self, _):
        button = self.ids.reset_button 
        button.disabled = False 


    def executar(self):
        IP = self.inputIP.text
        username = "admin"
        password = self.inputSenha.text
        url = f"http://{IP}:80/cgi-bin/magicBox.cgi?action=getDeviceType"
        try:
            response = requests.get(url, timeout= 5)
            self.ids.response_msg = ""
            if response.status_code == 401:
                auth_params = response.headers.get('WWW-Authenticate')
                realm = auth_params.split('realm="')[1].split('"')[0]
                nonce = auth_params.split('nonce="')[1].split('"')[0]
                qop = auth_params.split('qop="')[1].split('"')[0]
                opaque = auth_params.split('opaque="')[1].split('"')[0]

                cnonce = secrets.token_hex(8)

                nc = "00000002"

                hash_password = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()

                method = "GET"
                uri = url
                request_digest = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()

                response_digest = hashlib.md5(
                    f"{hash_password}:{nonce}:{nc}:{cnonce}:{qop}:{request_digest}".encode()
                ).hexdigest()

                authorization_header = (
                    f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
                    f'uri="{uri}", response="{response_digest}", qop={qop}, nc={nc}, cnonce="{cnonce}", opaque="{opaque}"'
                )

                response = requests.get(url, headers={'Authorization': authorization_header})

                if response.status_code == 200: #fim da captura de modelo
                    api_response = response.text
                    modeloCamera = api_response.replace("type=", "")
                    
                    url = f"http://{IP}:80/cgi-bin/magicBox.cgi?action=resetSystemEx&type=0"
                    response = requests.get(url)
                    if response.status_code == 401:
                        auth_params = response.headers.get('WWW-Authenticate')
                        realm = auth_params.split('realm="')[1].split('"')[0]
                        nonce = auth_params.split('nonce="')[1].split('"')[0]
                        qop = auth_params.split('qop="')[1].split('"')[0]
                        opaque = auth_params.split('opaque="')[1].split('"')[0]

                        cnonce = secrets.token_hex(8)

                        nc = "00000002"

                        hash_password = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()

                        method = "GET"
                        uri = url
                        request_digest = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()

                        response_digest = hashlib.md5(
                            f"{hash_password}:{nonce}:{nc}:{cnonce}:{qop}:{request_digest}".encode()
                        ).hexdigest()

                        authorization_header = (
                            f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
                            f'uri="{uri}", response="{response_digest}", qop={qop}, nc={nc}, cnonce="{cnonce}", opaque="{opaque}"'
                        )

                        response = requests.get(url, headers={'Authorization': authorization_header})

                        if response.status_code == 200:
                            self.responseMsg.text = f"Câmera {modeloCamera} resetada com sucesso!"
                            
                        else:
                            self.responseMsg.text = "erro"
                            
                else:
                    self.responseMsg.text = "IP ou senha inválidos"
                    

            else:
                self.responseMsg.text = "IP ou senha inválidos"
                
        except requests.exceptions.RequestException as e:
                self.responseMsg.text = (f"Erro na requisição: Verifique o IP e senha do dispositivo.")
                
class Inicio(Screen):
    pass
    
APIReset().run()

#teste1