from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from . import serializers
from .parser import Parser


class ParserViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ParserSerializer

    @action(detail=False, methods=['POST'])
    def run(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['text']
            return Response({'conditions': Parser().parse(input_text)})
        else:
            return Response(serializer.errors, status=400)


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer

    @action(detail=False, methods=['GET'])
    def current(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)