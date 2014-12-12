# -*- coding: utf-8 -*-
import uuid
import os

from lxml import etree as cet
from Cheetah.Template import Template


def parse_data_from_file(in_file_name):
    root = cet.parse(in_file_name, parser=cet.XMLParser(encoding='utf-8')).getroot()
    results = {
        "suite_name": root.attrib.get('name', 'NONAME') + " || " + in_file_name,
        "total_run": root.attrib.get('tests', 0),
        "errored": root.attrib.get('errors', 0),
        "failed": root.attrib.get('failures', 0),
        "skipped": root.attrib.get('skip', 0),
        "time": root.attrib.get('time', -1),
        "id": str(uuid.uuid4())
    }
    results["testcases"] = []
    for tc in (t for t in root.getchildren() if t.tag == u'testcase'):
        testcase = {
            "name": tc.attrib['classname'] + "." + tc.attrib['name'],
            "time": tc.attrib['time'],
            "id": (tc.attrib['classname'] + "." + tc.attrib['name']).replace('.', '_'),
            #Possibly needlessly hacky way of getting the last element of the list if
            #it is present. There should only be one element if there is one at all
            "info": get_testrun_info(tc),
        }
        results["testcases"].append(testcase)
    return results


def get_testrun_info(testcase):
    failure_info = [
        {
            "msg": {
                "skipped": "was skipped : " + tcinfo.attrib.get('type', 'NOINFO'),
                "error": "encountered an error : " + tcinfo.attrib.get('type', 'NOINFO'),
                "failed": "failed : " + tcinfo.attrib.get('type', 'NOINFO'),
                "failure": "failed : " + tcinfo.attrib.get('type', 'NOINFO')
            }.get(tcinfo.tag, "Unrecognized tag type {0}".format(tcinfo.tag)),
            "data": tcinfo.attrib.get("message", 'NOMESSAGE') + ":\n" + unicode(tcinfo.text).encode('utf-8'),
            "type": tcinfo.tag
        } for tcinfo in testcase.getchildren()
        if tcinfo.tag in ["skipped", "error", "failed", "failure"]
    ]

    if not failure_info:
        runinfo = {
            "msg": "was successful",
            "data": "",
            "type": "success"
        }
    else:  # Get stdout and stderr if pytest-run
        runinfo = failure_info[0]  # There is only ever a single failure-mode element
        for tcinfo in testcase.getchildren():
            if tcinfo.tag not in ["skipped", "error", "failed", "failure"]:
                runinfo["data"] += "\n---{0}---\n{1}".format(tcinfo.tag, unicode(tcinfo.text).encode('utf-8'))

    return runinfo


def full_path_of(in_file_name):
    """Translates a relative path to a full path based on the assumption that the relative
    path is intended relative to this (xunit2html.py) file."""
    return os.path.join(os.path.dirname(__file__), in_file_name)


def render_report(in_xunit_file_names, show_successes=False):
    suites = [parse_data_from_file(filename) for filename in in_xunit_file_names]
    return str(Template(file=full_path_of("templates/report.tmpl"),
                        searchList=[
                            {
                                "testsuites": [str(Template(file=full_path_of("templates/testsuite.tmpl"), searchList=[suite, {"show_successes": show_successes}])) for suite in suites],
                                "suite_listing": str(Template(file=full_path_of("templates/suite_listing.tmpl"), searchList=[{"testsuites": suites}])),
                                "stylesheet": open(full_path_of("templates/report.css")).read(),
                                "jquery": open(full_path_of("templates/jquery-1.9.1.min.js")).read()
                            }
                        ]))
