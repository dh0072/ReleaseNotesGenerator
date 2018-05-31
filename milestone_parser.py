"""
Milestone Request

The milestone request provides a list of ticket numbers in the milestone. The
request query needs to be modified from the one on the wiki page to include all
ticket states. The report needs to contain all tickets, open, closed, etc for
that release.

There should be a single class to handle this. Please do not use inheritance,
contains by use or reference is OK. The class generates a list of ticket numbers
and this is the exported interface via a method in the class.
"""

from parse_html import TracHTMLParser
import urllib.request
from datetime import datetime


class MilestoneParser():
    def __init__(self, rtems_url_base="https://devel.rtems.org", milestone="milestone"):
        self.rtems_url_base = rtems_url_base
        self.milestone = milestone

    def get_milestone_stats(self, milestone_id):
        milestone_stats = {}
        milestone_url = "/".join([self.rtems_url_base, self.milestone, milestone_id])
        trac_html_parser = TracHTMLParser()
        bs = trac_html_parser.parse_page(milestone_url)

        milestone_stats["milestone_id"]=milestone_id
        title_tag = bs.find(name="div", attrs={"id": "content", "class": "milestone"}).find(name="h1")
        milestone_stats["title"] = title_tag.text if title_tag else None

        timeline_tag = bs.find(name="p", attrs={"class": "date"})
        milestone_stats["timeline"] = timeline_tag.contents[-1].strip() if timeline_tag else None

        percent_tag = bs.find(name="p", attrs={"class": "percent"})
        milestone_stats["percent"] = percent_tag.string if percent_tag else None

        nums_tag = bs.find(name="span", attrs={"class": "first interval"})
        milestone_stats["total_tickets_num"] = nums_tag.find(name="a").string if nums_tag else None

        tickets_list_url = "/".join([self.rtems_url_base, nums_tag.find(name="a")["href"]])
        milestone_stats["tickets_list"] = self._get_tickets_list(tickets_list_url)
        return milestone_stats

    def _get_tickets_list(self, tickets_list_url):
        tickets_list = []
        trac_html_parser = TracHTMLParser()

        bs = trac_html_parser.parse_page(tickets_list_url)
        all_rows = bs.find(name="table", attrs={"class": "listing tickets"}).find(name="tbody").find_all(name="tr")

        # parse each row to get ticket id, summary, owner, type etc.
        for row in all_rows:
            id = row.find(name="td", attrs={"class": "id"}).string.strip()
            summary = row.find(name="td", attrs={"class": "summary"}).find(name="a").string.strip()
            owner_tag = row.find(name="td", attrs={"class": "owner"})
            span_tag = owner_tag.find(name="span", attrs={"class": "usernamedecorate-anonymous"}) if owner_tag else None
            owner = span_tag.string.strip() if span_tag else None
            type = row.find(name="td", attrs={"class": "type"}).string.strip()
            priority = row.find(name="td", attrs={"class": "priority"}).string.strip()
            component = row.find(name="td", attrs={"class": "component"}).string.strip()
            version = row.find(name="td", attrs={"class": "version"}).string.strip()
            tickets_list.append({"id": id, "summary": summary, "owner": owner, "type": type, "priority": priority, "component": component, "version": version})
        return tickets_list


# This is for test purpose
mtp = MilestoneParser()
import pprint
pp = pprint.PrettyPrinter(indent=4)
milestone_stats = mtp.get_milestone_stats(milestone_id="4.11.3")
pp.pprint(milestone_stats)
