from spyne import ServiceBase, rpc, String, Integer
from services.services import create_dog_service, get_dog_by_id_service

class ResourceService(ServiceBase):

    @rpc(String, String, String, String, String, String, _returns=String)
    def create_dog(ctx, name, gender, size, weight, birth_date, adopted):
        #SOAP endpoint to create a dog resource.
        #Test the endpoint
        """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:create_dog>
                <soap:name>Max</soap:name>
                <soap:gender>Male</soap:gender>
                <soap:size>Large</soap:size>
                <soap:weight>30.5</soap:weight>
                <soap:birth_date>2020-05-01</soap:birth_date>
                <soap:adopted>false</soap:adopted>
            </soap:create_dog>
        </soapenv:Body>
        </soapenv:Envelope>
        """
        return create_dog_service(name, gender, size, weight, birth_date, adopted)

    @rpc(Integer, _returns=String)
    def get_dog_by_id(ctx, dog_id):
        #SOAP endpoint to fetch a dog resource by ID.
        # Test the endpoint
        """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:get_dog_by_id>
                <soap:dog_id>1</soap:dog_id>
            </soap:get_dog_by_id>
        </soapenv:Body>
        </soapenv:Envelope>
        """ 
        return get_dog_by_id_service(dog_id)
