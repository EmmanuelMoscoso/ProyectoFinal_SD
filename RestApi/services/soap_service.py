from zeep import Client

SOAP_URL = 'http://proyectofinal_sd-api-soap-1:8000/?wsdl'

soap_client = Client(SOAP_URL)

def create_user_soap(name, age, email, phone):
    return soap_client.service.create_user(name, age, email, phone)

def get_user_by_id_soap(user_id):
    return soap_client.service.get_user_by_id(user_id)