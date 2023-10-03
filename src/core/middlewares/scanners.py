import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class AvailableScannersMiddleware(object):
    """
    This is a strict middleware for scanner's requests.
    The following checks are implemented:
        1) Is the request scanner available?
        2) Does the requested endpoint, matches the given scanner requests
           in the form data? Why, because of target parameter rules on
           serializer (validation step, this is why the number is needed)

    If either of the checks do not pass, this returns a vauge 400 response.
    """

    def __init__(self, get_response):
        self.get_response = get_response


    def is_scanner_available(self, path, request):
        scanner = request.POST.get("scanner", None)
        message = "Invalid request."

        if scanner is None:
            return self.return_response(request, message)

        if settings.SCANNERS_AVAILABLE.get(int(scanner)) is None:
            return self.return_response(request, message)
        
        check = self.map_scanner_scanners_availalble(path, scanner)
        if not check[0]:
            message = check[1]
            return self.return_response(request, message)

        return True, None


    def map_scanner_scanners_availalble(self, path, scanner):
        split_path = path.split("/")
        scanner_path = split_path[-2]
        logger.info(scanner_path)
        if not settings.SCANNERS_AVAILABLE[int(scanner)] == scanner_path:
            return False, "Invalid request, check url and data."
        return True, None


    def return_response(self, request, message):
        view = APIView()
        view.headers = view.default_response_headers
        response = Response(
            {"status" : False, "message" : message},
            status=400,
        )
        return False, view.finalize_response(request, response).render()


    def __call__(self, request):
        path = request.path
        method = request.method
        
        if '/scanners/' in path and method == "POST":
            t1 = self.is_scanner_available(path, request)
            if not t1[0]:
                return t1[1]
        
        response = self.get_response(request)
        return response
