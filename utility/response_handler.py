from rest_framework import status
from rest_framework.response import Response


class ResponseSchema:

    def __init__(self, data, success, status_code):
        self.data = data
        self.success = success
        self.status_code = status_code

    def getResponse(self):
        return Response({
            'status_code': self.status_code,
            'status': self.success,
            'response': self.data,
        }, status=self.status_code)


class HTTPResponse:

    def __init__(self, status_code=None):
        self.__status_code=status_code if status_code is not None else status.HTTP_200_OK

    def unauthorized(desc):
        response= ResponseSchema('HTTP_401_UNAUTHORIZED', 'error',
                          status.HTTP_401_UNAUTHORIZED)
        return response.getResponse()

    def bad_request(desc, data):
        response= ResponseSchema(data, 'error',
                          status.HTTP_400_BAD_REQUEST)
        return response.getResponse()

    def internal_server_error(desc,data):
        response= ResponseSchema(data,'error', status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.getResponse()

    def success_response(self, data):
        response=ResponseSchema(data, 'success', status.HTTP_200_OK)
        return response.getResponse()

    def not_found(self, data):
        response=ResponseSchema(data, 'error', status.HTTP_404_NOT_FOUND)
        return response.getResponse()

    def forbidden(self, data):
        response=ResponseSchema(data, 'error', status.HTTP_403_FORBIDDEN)
        return response.getResponse()

    def generic_response(self,data):
        if self.__status_code==401:
            return self.unauthorized()
        if self.__status_code==400:
            return self.bad_request(data)
        if self.__status_code==200 or self.__status_code==201 or self.__status_code==204:
            return self.success_response(data)
        if self.__status_code==404:
            return self.not_found(data)
        if self.__status_code==500:
            return self.internal_server_error(data)
        if self.__status_code==403:
            return self.forbidden(data)