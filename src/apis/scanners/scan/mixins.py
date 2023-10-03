"""
Міксини для моделей адміністратора (дисплеї)
"""

class ScanTextReports(object):
    """
    Для простоти текстові звіти містяться в цьому класі лише для того, щоб розділити
    функціональність між класами

    Деякі звіти містять додаткову інформацію про те, як використовувати результати.
    """

    def dirbpy_text_report(self):
        return "Not implemented yet"
 
    def sslyze_text_report(self):
        scan_type = self.meta.get("scan_type")
        if scan_type is None:
            return "Unable to get scan results."

        parent_scan, msg = self.parent_scan()
        if not parent_scan:
            return msg

        if scan_type == "simple":
            data = self.sslyze_simple_scan_results
            heartbleed = data.get("heartbleed_detected")
            openssl_ccs = data.get("openssl_ccs_injection")
            robot_result = data.get("robot")
            renegotiation = data.get("session_renegotiation")
            vulnerable_renegotiation = renegotiation.get("is_vulnerable_to_client_renegotiation")
            secure_renegotiation = renegotiation.get("supports_secure_renegotiation")

            ##############################################################
            # Напишіть невеликий звіт із результатами сканування
            ##############################################################

            text = ("#" * 80) + "\n"
            text += "Simple scan report for %s\n" % parent_scan.target
            text += ("#" * 80) + "\n"
            text += "Heartbleed detected: <span style='color: white;%s'>%s</span>.\n" % (
                'background-color: red;' if not heartbleed else 'background-color: green;',
                heartbleed,
            )
            text += "<a href='https://exploit-db.com/docs/49313'>Check this paper</a> "
            text += "for info on how to exploit this vulnerability, need msfconsole.\n"
            text += ("#" * 80) + "\n"
            text += "Openssl ccs injection detected: <span style='color: white;%s'>%s</span>.\n" % (
                'background-color: red;' if not openssl_ccs else 'background-color: green;',
                openssl_ccs
            )
            text += ("#" * 80) + "\n"
            text += "Robot result: %s.\n" % robot_result
            text += ("#" * 80) + "\n"
            text += "Vulnerable to renegotiation: %s\n" % vulnerable_renegotiation
            text += ("#" * 80) + "\n"
            text += "Suports secure renegotiation: %s\n" % secure_renegotiation 
        elif scan_type == "full":
            data = self.sslyze_full_scan_results
            # TO DO
            text = "Full scan report not supported yet."
        return text

    def wafw00f_text_report(self):
        if not self.data.get('status'):
            error = self.data.get('error')
            return "Error occured: %s " % error
        context = "WAF scan report for scan %s" % self.uid
        wafs = self.data.get('data')
        for i, waf in enumerate(wafs, start=1):
            waf_detected = waf.get("detected", False)
            if not waf_detected:
                if len(wafs) == 1:
                    context += "\n\n%s No waf detected for %s \n\n" % (
                        i,
                        waf.get('url')
                    )
                    break
                continue
            firewall = waf.get("firewall")
            url = waf.get("url")
            trigger_url = waf.get("trigger_url")
            if trigger_url == True: # need to strict check for boolean
                trigger_url = "Generic (from site) %s" % url
            context += "\n\n%s WAF: %s detected at target: %s\n" % (i, firewall, url)
            context += "\nUrl that triggered the WAF: %s" % trigger_url
        return context

    def whatweb_text_report(self):
        return ""
       

class ScanParser(ScanTextReports):
    """
    Усі методи повертають словники Python із ключовими результатами сканування для
    звітів.
    """
    @property
    def dirby_simple_scan_results(self):
        return {}
    
    @property
    def dirby_full_scan_results(self):
        return {}

    @property
    def sslyze_simple_scan_results(self):
        """
        Зробіть технічне сканування наполовину технічним і наполовину читабельним
        звітом
        """
        if self.normalize_status != "Complete":
            return "No data for this scan, status %s -- check raw json for detatils." % (
                self.normalize_status
            )
        #################################################################
        # Оголошіть деякі змінні, які містять те, що ми перевіряємо під 
        # час простого сканування
        #################################################################
        certificate_info = None
        elliptic_curves = None
        heartbleed = None
        http_headers = None
        openssl_ccs_injection = None
        robot = None
        session_renegotiation = None
        tls_compression = None

        data = self.data.get("data")
        scan_completed = data.get("date_scans_completed")
        scan_started = data.get("date_scans_started")
        scan_results = data.get("server_scan_results")
        for result in scan_results:
            for key, value in result.items():
                if key != "scan_result":
                    continue
                certificate_info = value.get("certificate_info")
                elliptic_curves = value.get("elliptic_curves")
                heartbleed = value.get("heartbleed")
                http_headers = value.get("http_headers")
                openssl_ccs_injection = value.get("openssl_ccs_injection")
                robot = value.get("robot")
                session_renegotiation = value.get("session_renegotiation")
                break

        return {
            'heartbleed_detected' : heartbleed.get(
                "result", {}
            ).get(
                "is_vulnerable_to_heartbleed", False
            ),
            'openssl_ccs_injection' : openssl_ccs_injection.get(
                "result", {}
            ).get(
                "openssl_ccs_injection", False
            ),
            'robot' : robot.get(
                "result", {}
            ).get(
                "robot_result", False
            ),
            'session_renegotiation' : {
                'renegotiation' : session_renegotiation.get(
                    "result", {}
                ).get(
                    'is_vulnerable_to_client_renegotiation', False
                ),
                'supports_secure_renegotiation' : session_renegotiation.get(
                    'result', {}
                ).get(
                    'supports_secure_renegotiation', True
                )
            }
        }
    
    @property
    def sslyze_full_scan_results(self):
        return {}

    @property
    def whatweb_simple_scan_results(self):
        return {}

    @property
    def whatweb_full_scan_results(self):
        return {}

