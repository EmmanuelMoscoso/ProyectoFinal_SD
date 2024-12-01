from spyne import ServiceBase, rpc, String, Integer
from services.services import create_user_service, get_user_by_id_service

class ResourceService(ServiceBase):

    @rpc(String, String, String, String, _returns=String)
    def create_user(ctx, name, age, email, phone):
        # SOAP endpoint to create a user resource.
        # Example to test the endpoint
        """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:create_user>
                <soap:name>Max</soap:name>
                <soap:age>32</soap:age>
                <soap:email>max@gmail.com</soap:email>
                <soap:phone>4420123456</soap:phone>
            </soap:create_user>
        </soapenv:Body>
        </soapenv:Envelope>
        """
        return create_user_service(name, age, email, phone)

    @rpc(Integer, _returns=String)
    def get_user_by_id(ctx, user_id):
        # SOAP endpoint to get a user by ID.
        # Example to test the endpoint
        """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:get_user_by_id>
                <soap:user_id>1</soap:user_id>
            </soap:get_user_by_id>
        </soapenv:Body>
        </soapenv:Envelope>
        """ 
        return get_user_by_id_service(user_id)
