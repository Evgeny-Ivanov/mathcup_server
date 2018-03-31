import os
import hashlib
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    status,
    permissions
)
from . import serializers


class UploadView(viewsets.ViewSet):
    permission_classes = (permissions.IsAdminUser,)

    @staticmethod
    def generate_file_path(file):
        _, file_extension = os.path.splitext(file.name)
        sha_hash = UploadView.generate_sha(file)
        file_name = sha_hash + file_extension
        file_path = 'uploads/images/' + file_name

        return file_path

    @staticmethod
    def handle_uploaded_file(file, file_path):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def generate_sha(file):
        sha = hashlib.sha1()
        file.seek(0)
        while True:
            buf = file.read(104857600)
            if not buf:
                break
            sha.update(buf)
        sha1 = sha.hexdigest()
        file.seek(0)

        return sha1

    def upload_image(self, request):
        serializer = serializers.UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['image']
            file_path = self.generate_file_path(file)
            self.handle_uploaded_file(file, file_path)
            return Response(data={'link': '/' + file_path}, status=status.HTTP_200_OK)
