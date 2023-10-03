import logging

from urllib.parse import urlparse

from django.conf import settings
from ipaddress import ip_address
from rest_framework import serializers

from .rules import ScannersRules


logger = logging.getLogger(__name__)


class ScannerTargetSerializer(serializers.Serializer):
    """
    Checks if a scanner has been tasked with multiple scans
    or a single scan, and then validates each target.
    """
    target = serializers.CharField(required=True)
    scanner = serializers.IntegerField(required=True)
    
    def validate(self, data):

        scanner = settings.SCANNERS_AVAILABLE[data["scanner"]]
        value = data["target"].split(",")

        check = self.handle_targets(value, scanner)
        if not check[0]:
            message = "[%s] " % scanner.upper()
            for each in check[1]:
                each = each.strip(" ")
                message += "Invalid target found: %s | " % each
            message += "Read Documentation for usage."
            raise serializers.ValidationError(message)

        value = check[1]
        return {"scanner" : scanner, "target" : check[1]}


    def handle_targets(self, targets, scanner):
        """
        Checks for single or multiple targets.
            Is it ip or is it domain?
                Is this taget valid for the scanner?
        TO DO:
            Format the error message, with erroneous targets for the user.
        """
        all_checks = []
        clean_targets = []
        bad_targets = []
        for each in targets:
            each = each.strip(" ")
            is_ip = self.is_ip(each)
            is_domain = self.is_domain(each)

            if is_ip or is_domain:
                args = (each, scanner, is_ip, is_domain,)
                scanner_check = self.check_scanner_rules(*args)

                if not scanner_check[0]:
                    all_checks.append(False)
                    bad_targets.append(scanner_check[1])
                    continue

                all_checks.append(True)
                clean_targets.append(scanner_check[1])
                continue

            all_checks.append(False)
            bad_targets.append(each)
            continue

        if not all(all_checks):
            return False, bad_targets
        return True, clean_targets


    def check_scanner_rules(
            self, 
            target, 
            scanner, 
            is_ip, 
            is_domain
        ):
        """
        Every scanner has rules for the targets it takes.
        This method enforces those rules.
        """
        rules = ScannersRules()
        
        if scanner == "dirby":
            t = rules.dirby_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]
        
        elif scanner == "scanvus":
            t = rules.scanvus_rules(target, is_ip)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "sslyze":
            t = rules.sslyze_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "wafwoof":
            t = rules.wafwoof_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "wapiti":
            t = rules.wapiti_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "whatweb":
            t = rules.whatweb_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "zap":
            t = rules.zap_rules(target)
            if t[0]:
                return True, t[1]
            return False, t[1]

        elif scanner == "cvescannerv2":
            t = rules.cvescannerv2_rules(target, is_ip)
            if t[0]:
                return True, t[1]
            return False, t[1]
        
        return False, target


    def is_ip(self, target):
        """
        Tests if the ip has a scheme, not valid
        Tests if the is an actual IP
        """
        try:
            test = urlparse(target)
            if test.scheme in ['http', 'https']:
                raise ValueError
            ip_address(target)
        except ValueError:
            return False
        except Exception:
            return False
        return True


    def is_domain(self, target):
        try:
            result = urlparse(target)
            return all([result.scheme, result.netloc])
        except Exception:
            return False


class GetSingleScanSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
