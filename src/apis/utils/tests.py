import os
import unittest
from django.conf import settings
from django.test import TestCase

from .serializers import ScannerTargetSerializer



class TestScannerTargetSerializer(TestCase):
    
    def setUp(self):
        self.serializer = ScannerTargetSerializer
        self.scanners = settings.SCANNERS_AVAILABLE


    def test_multiple_good_targets_dirby(self):
        targets = ",".join([
            "http://10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "http://google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 1}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_dirby(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 1}
        )
        test_passes = test.is_valid(raise_exception=True)

 
    def test_multiple_good_targets_scanvus(self):
        targets = ",".join([
            "10.10.10.10",
            "150.234.52.10",
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 2}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_scanvus(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 2}
        )
        test_passes = test.is_valid(raise_exception=True)

    def test_multiple_good_targets_sslyze(self):
        targets = ",".join([
            "https://10.10.10.10",
            "https://google.com",
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 3}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_sslyze(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 3}
        )
        test_passes = test.is_valid(raise_exception=True)


    def test_multiple_good_targets_wapiti(self):
        targets = ",".join([
            "http://10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "http://google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 4}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_wapiti(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 4}
        )
        test_passes = test.is_valid(raise_exception=True)


    def test_multiple_good_targets_wafwoof(self):
        targets = ",".join([
            "http://10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "http://google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 5}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_wafwoof(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : 5}
        )
        test_passes = test.is_valid(raise_exception=True)

'''
    def test_multiple_good_targets_dirby(self):
        targets = ",".join([
            "http://10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "http://google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : self.scanners[1]}
        )
        test_passes = test.is_valid(raise_exception=True)


    @unittest.expectedFailure
    def test_multiple_wrong_targets_dirby(self):
        targets = ",".join([
            "10.10.10.10",
            "https://google.com",
            "http://150.234.52.10",
            "google.com"
        ])
        test = self.serializer(
            data={"target" : targets, "scanner" : self.scanners[1]}
        )
        test_passes = test.is_valid(raise_exception=True)
'''
