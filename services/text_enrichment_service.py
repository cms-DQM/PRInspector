import config
import re

def enrich_comment(body):
    if body == None or body == '':
        return '<em>No description provided.</em>'
    
    body = add_links_to_pr_numbers(body)
    body = add_links_to_urls(body)
    body = add_line_breaks(body)
    body = replace_code_tags(body)
    body = bold_usernames(body)

    return body

def add_links_to_pr_numbers(body):
    regex = r'( )(#)([0-9]+)'
    body = re.sub(regex, r'\1<a href="' + __get_pr_url(r'\3') + r'" target="_blank">\2\3</a>', body)
    return body

def add_links_to_urls(body):
    # body = re.sub(r'(http[s]?://(?:[a-zA-Z]|[0-9]|(?![,\(\)])[$-_@.&+#~]|[!*]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)', r'<a href="\1" target="_blank">\1</a>', body)
    regex = r'''([^"']|^)(https?:\/\/[-\w.%&?/:_@#=+;]+[^."')\s ])'''
    body = re.sub(regex, r'\1<a href="\2" target="_blank">\2</a>', body, flags=re.IGNORECASE)
    return body

def add_line_breaks(body):
    body = body.replace('\n', '<br>')
    return body

def replace_code_tags(body):
    regex = r'`(.*?)`'
    body = re.sub(regex, r'<code>\1</code>', body)
    return body

def bold_usernames(body):
    regex = r'(@[a-z\d]+-*[a-z\d]+)'
    body = re.sub(regex, r'<strong>\1</strong>', body, flags=re.IGNORECASE)
    return body

def __get_pr_url(pr_number):
    return config.get_repo_url() + 'pull/' + pr_number
