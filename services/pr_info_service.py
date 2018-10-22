import config
import re

def get_subsystem_in_title_info(title):
    subsystems = config.get_subsystems()

    for subsystem in subsystems:

        index = title.lower().find(subsystem.lower())
        if index != -1:
            opening = '<span class="text-info">'
            closing = '</span>'

            new_title = title[:index] + opening + title[index:index + len(subsystem)] + closing + title[index + len(subsystem):]
            return { 'text': 'Subsystem is in the title', 'class': 'text-success', 'enriched_title': new_title, 'description': "Name of known CMS subsystem is mentioned in the title of this PR" }
    
    return { 'text': 'Subsystem is not in the title', 'class': 'text-danger', 'enriched_title': title, 'description': "Known CMS subsystem is not mentioned in the title of this PR. Specifying a subsystem in the title is considered to be a good practise" }
