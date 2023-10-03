""" 
**********************************************************************
Кожен сканер отримує завдання <сканер>_task та <сканер>_scan, 
перше - це демон, а друге - виконавець. Це, можливо, дуже повторювано, 
але для цього я вважаю за краще бути явним.
**********************************************************************
""" 

import json
import logging
import subprocess

from apis.scanners.scan.models import Scan
from proxies.models import ProxyConfig


logger = logging.getLogger(__name__)


class DockerExec(object):
    """
    Використовується для запуску команди run у контейнері
    з машини-хоста через гніздо Docker (підключене).
    """
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)
        self.http_tunnel = None
        self.set_http_tunnel()

    def set_http_tunnel(self):
        proxies = ProxyConfig.objects.filter(
            meta__is_main=True, 
            is_active=True
        )
        if proxies.exists():
            self.http_tunnel = proxies.first()
            return True
        return False

    def run(self, options):
        action = subprocess.run(
            options,
            capture_output=True
        )
        if action.returncode == 0:
            return True, action.stdout.decode('utf-8').strip('\n')
        return False, action.stderr.decode('utf-8').strip('\n')

    def wafwoof_scan(self, scan_obj):
        if self.http_tunnel is not None:
            command = "docker run --rm --network obsidiana wafw00f "
            command += "--proxy %s " % self.http_tunnel.as_url
        else:
            command = "docker run --rm wafw00f "
        if hasattr(self, 'extra_options'):
            for opt in self.extra_options: command += "%s " % opt
        command += self.target
        command = command.split(' ')
        scan_obj.status = "RU"
        scan_obj.save()
        result, scan = self.run(command)
        if result:
            scan_obj.status ="DO"
            scan_obj.save()
            return {'status' : True, 'data' : scan}
        scan_obj.status = "FL"
        scan_obj.save()
        return {'status' : False, 'data' : {'error' : scan}}
    
    @staticmethod
    def wafwoof_task(data):
        obj = data.get('obj')
        scan_type = data.get('scan_type')
        scan_obj = data.get('scan_obj')
        if scan_type == "full":
            extra_options = [
                '--findall', # не зупиняється на першому веб-фаєрволі додатка
            ]
            bridge = DockerExec(**{
                'target' : obj.target, 
                'extra_options' : extra_options
            })
        elif scan_type == "simple":
            bridge = DockerExec(**{'target' : obj.target})
        action = bridge.wafwoof_scan(scan_obj)
        try:
            if action["status"]:
                action["data"] = json.loads(action["data"])
        except json.JSONDecodeError as error:
            try:
                action["data"] = eval(action["data"])
            except Exception as eval_error:
                action["data"] = {
                    "errors" : [str(error), str(eval_error)],
                    "action" : str(action["data"])
                }
        meta = {
            'scanner' : 'wafw00f',
            'parent_scan_pk' : obj.pk,
            'scan_type' : scan_type 
        }
        if not Scan.save_scan_result(meta, action, scan_obj):
            logger.info("Unable to create scan and add it to scanner %s" % obj) 
            return False
        return True
   
    def sslyze_scan(self, scan_obj):
        if self.http_tunnel is not None:
            command = "docker run --rm --network obsidiana sslyze --json_out=- "
            command += "--https_tunnel=%s " % self.http_tunnel.as_url
        else:
            command = "docker run --rm sslyze --json_out=- "
        if hasattr(self, 'extra_options'):
            for opt in self.extra_options: command += "%s " % opt
        command += self.target
        command = command.split(' ')
        scan_obj.status = "RU"
        scan_obj.save()
        result, scan = self.run(command)
        if result:
            scan_obj.status ="DO"
            scan_obj.save()
            return {'status' : True, 'data' : scan}
        scan_obj.status = "FL"
        scan_obj.save()
        return {'status' : False, 'data' : {'error' : scan}}
    
    @staticmethod
    def sslyze_task(data):
        obj = data.get('obj')
        scan_type = data.get('scan_type')
        scan_obj = data.get('scan_obj')
        if scan_type == "full":
            #############################################################
            # Відсутність параметрів виклику спричинює сканування всього.
            #############################################################
            bridge = DockerExec(**{'target' : obj.target,})
        elif scan_type == "simple":
            ##################################
            # Надання лише простих параметрів.
            ##################################
            extra_options = [
                "--heartbleed", # test 4 heartbleed vuln
                "--http_headers", # test 4 insecure headers
                "--reneg", # test 4 isnecure renegotiation
                "--robot", # test 4 ROBOT vuln
                "--openssl_ccs", # test 4 openssl CCS INJECTION (CVE-2014-0224)
                "--compression" # test 4 CRIME attack, no TLS support only.
            ]
            bridge = DockerExec(**{
                'target' : obj.target, 
                'extra_options' : extra_options
            })
        action = bridge.sslyze_scan(scan_obj)
        try:
            if action["status"]:
                action["data"] = json.loads(action["data"])
        except json.JSONDecodeError as error:
            try:
                action["data"] = eval(action["data"])
            except Exception as eval_error:
                action["data"] = {
                    "errors" : [str(error), str(eval_error)],
                    "action" : str(action["data"])
                }
        meta = {
            'scanner' : 'sslyze',
            'parent_scan_pk' : obj.pk,
            'scan_type' : scan_type 
        }
        if not Scan.save_scan_result(meta, action, scan_obj):
            logger.info(
                "Unable to create scan and add it to scanner %s" % obj
            ) 
            return False
        return True

    def dirbpy_scan(self, scan_obj, scan_type):
        command = "docker run --rm dirbpy "
        if hasattr(self, 'extra_options'):
            for opt in self.extra_options: command += "%s " % opt
        command += "-u %s" % self.target
        command = command.split(' ')
        scan_obj.status = "RU"
        scan_obj.save()
        result, scan = self.run(command)
        if result:
            scan_obj.status ="DO"
            scan_obj.save()
            return {'status' : True, 'data' : scan}
        scan_obj.status = "FL"
        scan_obj.save()
        return {'status' : False, 'data' : {'error' : scan}}
    
    @staticmethod
    def dirbpy_task(data):
        obj = data.get('obj')
        scan_type = data.get('scan_type')
        scan_obj = data.get('scan_obj')
        if scan_type == "full":
            #######################################
            # Займає багато часу, повідомте агента.
            #######################################
            extra_options = [
                "--directory=/files",
                "--thread=10",
                "--save=/out.json",
                "--remove-status-code=[503]"
            ]
            bridge = DockerExec(**{
                'target' : obj.target, 
                'extra_options' : extra_options
            })
        elif scan_type == "simple":
            ###########################################################
            # Мінімальний набір параметрів для тестування Apache, PHP 
            # та загальних URL-адрес:
            ###########################################################
            extra_options = [
                "--file=/files/minimal.txt",
                "--thread=3",
                "--save=/out.json",
                "--remove-status-code=[503]"
            ]
            bridge = DockerExec(**{
                'target' : obj.target, 
                'extra_options' : extra_options
            })
        action = bridge.dirby_scan(scan_obj)
        try:
            if action["status"]:
                action["data"] = json.loads(action["data"])
        except json.JSONDecodeError as error:
            try:
                action["data"] = eval(action["data"])
            except Exception as eval_error:
                action["data"] = {
                    "errors" : [str(error), str(eval_error)],
                    "action" : str(action["data"])
                }
        meta = {
            'scanner' : 'sslyze',
            'parent_scan_pk' : obj.pk,
            'scan_type' : scan_type 
        }
        if not Scan.save_scan_result(meta, action, scan_obj):
            logger.info("Unable to save scan data %s" % obj) 
            return False
        return True 
