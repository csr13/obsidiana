"""
Rules for the scanners, only checks if the target being sent to the
scanner of choice is valid for it, meaning it is sent in the right
format, this object is used in the ScannerTargetSerializer only.

This class is used for admin action and api entrypoint for serializers
validations.
"""

import logging
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)


class ScannersRules(object):

    def dirby_rules(self, target):
        """Dirby only takes host names without protocol"""
        copy_target = target
        target = urlparse(target)
        if target.scheme in ["http", "https"]:
            return True, copy_target
        return False, "Invalid target found %s" % copy_target


    def scanvus_rules(self, target, is_ip):
        """Scanvus only takes remote host addresses (IP) no scheme"""
        copy_target = target
        target = urlparse(target)
        if target.netloc == '' and is_ip:
            return True, copy_target
        return False, "Invalid target found %s" % copy_target


    def sslyze_rules(self, target):
        """SSLyze only checks for targets without protocol scheme"""
        if target.startswith("https://") or target.startswith("http://"):
            return False, "Invalid target, targets without protocol"
        try:
            test = requests.get("https://%s" % target)
        except Exception as error:
            return False, "Unable to register, target not reachable"
        if test.status_code not in [x for x in range(200, 600)]:
            return False, "Invalid target found %s only https" % target
        return True, target


    def wafwoof_rules(self, target):
        """wafw00f only takes host names and ips with protocol"""
        copy_target = target
        target = urlparse(target)
        if target.scheme in ["http", "https"]:
            return True, copy_target
        return False, "Invalid target found %s, only targets with schemes." % copy_target


    def wapiti_rules(self, target):
        copy_target = target
        target = urlparse(target)
        if target.scheme in ["http" , "https"]:
            return True, copy_target
        return False, "Invalid target detected %s only https|http" % copy_target


    def whatweb_rules(self, target):
        copy_target = target
        target = urlparse(target)
        if target.scheme in ["http", "https"]:
            return True, copy_target
        return False, "Invalid target detected %s only http|https" % copy_target


    def zap_rules(self, target):
        copy_target = target
        target = urlparse(target)
        if target.scheme in ["http", "https"]:
            return True, copy_target
        return False, "Invalid target detected %s only http|https" % copy_target


    def cvescannerv2_rules(self, target):
        raise NotImplementedError()


