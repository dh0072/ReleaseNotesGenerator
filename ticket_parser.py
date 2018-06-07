from parse_html import TracHTMLParser


class TicketParser():
    def __init__(self, ticket_id, rtems_url_base="https://devel.rtems.org", ticket="ticket"):
        self.ticket_id = ticket_id
        self.rtems_url_base = rtems_url_base
        self.ticket = ticket

    def get_ticket_meta(self):
        # store ticket id, summary, owner, type, priority, compnonent, version etc to a dict
        ticket_meta = {}
        ticket_url = "/".join([self.rtems_url_base, self.ticket, self.ticket_id])

        trac_html_parser = TracHTMLParser()
        bs = trac_html_parser.parse_page(ticket_url)
        # parse html to get ticket id, summary, owner, type etc and save them in ticket_meta dict
        ticket_meta["id"] = self.ticket_id

        status_tag = bs.find(name="span", attrs={"class": "trac-status"}).find(name="a")
        ticket_meta["status"] = None if status_tag is None else status_tag.string

        type_tag = bs.find(name= "span", attrs={"class": "trac-type"}).find(name="a")
        ticket_meta["type"] = None if type_tag is None else type_tag.string

        resolution_tag = bs.find(name= "span", attrs={"class": "trac-resolution"}).find(name="a")
        ticket_meta["resolution"] = None if resolution_tag is None else resolution_tag.string

        summary_tag = bs.find(name="span", attrs={"class": "summary"})
        ticket_meta["summary"] = None if summary_tag is None else summary_tag.string

        reporter_tag = bs.find(name="a", attrs={"class": "trac-author"})
        ticket_meta["reporter"] = None if reporter_tag is None else reporter_tag.string

        owner_tag = bs.find(name="span", attrs={"class": "usernamedecorate-anonymous"})
        ticket_meta["owner"] = None if owner_tag is None else owner_tag.string

        priority_tag = bs.find(name="td", attrs={"headers": "h_priority"}).find(name="a")
        ticket_meta["priority"] = None if priority_tag is None else priority_tag.string

        milestone_tag = bs.find(name="td", attrs={"headers": "h_milestone"}).find(name="a")
        ticket_meta["milestone"] = None if milestone_tag is None else milestone_tag.string

        component_tag = bs.find(name="td", attrs={"headers": "h_component"}).find(name="a")
        ticket_meta["component"] = None if component_tag is None else component_tag.string

        version_tag = bs.find(name="td", attrs={"headers": "h_version"}).find(name="a")
        ticket_meta["version"] = None if version_tag is None else version_tag.string

        severity_tag = bs.find(name="td", attrs={"headers": "h_severity"}).find(name="a")
        ticket_meta["severity"] = None if severity_tag is None else severity_tag.string

        keywords_tag = bs.find(name="td", attrs={"headers": "h_keywords", "class": "searchable"}).find(name="a")
        ticket_meta["keywords"] = None if keywords_tag is None else keywords_tag.string

        cc_tag = bs.find(name="td", attrs={"headers": "h_cc", "class": "searchable"}).find(name="a")
        ticket_meta["cc"] = None if cc_tag is None else cc_tag.string

        blocker_tag = bs.find(name="td", attrs={"headers": "h_blockedby"}).find(name="a")
        ticket_meta["blocker"] = None if blocker_tag is None else blocker_tag.string

        blocking_tag = bs.find(name="td", attrs={"headers": "h_blocking"}).find(name="a")
        ticket_meta["blocking"] = None if blocking_tag is None else blocking_tag.string

        description_tag = bs.find(name="div", attrs={"class": "description"}).find(name="div", attrs={"class": "searchable"}).find("p")
        ticket_meta["description"] = None if description_tag is None else description_tag.getText()

        ticket_meta["comments"] = self._parse_ticket_comments(bs)
        ticket_meta["attachments"] = self._parse_ticket_attachments(bs)
        return ticket_meta

    def _parse_ticket_comments(self, bs):
        comments = []
        comments_list = bs.find_all(name="div", attrs={"class": "change"})

        for i in range(len(comments_list)):
            commenter = comments_list[i].find(name="span", attrs={"class": "usernamedecorate-anonymous"}).text
            time = comments_list[i].find(name="a", attrs={"class": "timeline"}).string

            # comment can be empty, so check if "comment searchable”exists upfront
            comment_tag = comments_list[i].find(name="div", attrs={"class": "comment searchable"})
            comment = comment_tag.find(name="p").getText() if comment_tag else None
            comments.append({"id": i + 1, "commenter": commenter, "time": time, "comments": comment})
        return comments

    def _parse_ticket_attachments(self, bs):
        attachments_urls = []
        attachments_list_tag = bs.find_all(name="dl", attrs={"class": "attachments"})
        for attachment_tag in attachments_list_tag:
            attachments_urls.append(self.rtems_url_base + attachment_tag.find(name="dt").find(name="a")["href"])
        return attachments_urls


# This is for test purpose
tp = TicketParser(ticket_id="2802")
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tp.get_ticket_meta())
