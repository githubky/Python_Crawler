import requests

class WebCode:
    text=""

    def getWebCode(self,URL):
        self.text=requests.get(URL).text
