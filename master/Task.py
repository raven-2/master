import re
from datetime import datetime

import parsedatetime as pdt


def parse_date(date):
    """ Generate a more human-readable title.

    Returns:
        A string showing the date in Y-m-d format and the weekday.

    Raises:
        ValueError if date could not be parsed.
    """
    cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
    d, flag = cal.parse(date)

    if not flag:
        raise ValueError('The date "{}" could not be parsed.'.format(date))

    d = datetime(*d[:3])

    days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    return '{}-{:02d}-{:02d}, {}'.format(d.year, d.month, d.day, days[d.weekday()])


class Task:
    """ Represents a task.

    Every task, at a minimum, has a title, creator, ID, stage, assignee,
    project name, and tags.
    """
    def __init__(self, title, description, attributes=None, **kwargs):
        """ Init a new Task.

        Args:
            title: Title of the task.
            description: A longer description about the task.
            attributes: Metadata about the task. Each task is required to have
                the following attributes at a minimum.

                creation_date: String representing the task's creation date.
                    Can be human-readable; like 'today', or 'last wednesday'.
                creator: The userid of the person who created the task.
                id: The task's ID. It is on the creator to ensure it is unique.
                project: Name of the project which owns the task
                stage: What stage the task is in. Defaults to "todo".
                tags: List of tags for the task.

                These attributes may also be provided to the constructor via
                keyword arguments. Tasks may have additional attributes.

        Raises:
            ValueError if some attributes were invalid (see Task.check method).
        """
        attributes = attributes or dict()

        self.title = title
        self.description = description

        # Process attributes
        self.attributes = {}
        self.attributes.update(attributes)
        self.attributes.update(kwargs)

        self.check()
        self.refresh()

    def refresh(self):
        """ Make minor corrections to attribute values.

        Sort and downcase the tags and try to parse dates.

        Raises:
            ValueError if a date could not be parsed. This will happen if
                the value is a non-empty string that was not a parsable date.
        """
        if 'tags' in self.attributes:
            tags = sorted(list(set([x.lower() for x in self.attributes['tags']])))
            self.attributes['tags'] = tags

        # Try to parse dates
        for k, v in self.attributes.items():
            if 'date' in k and v:
                self.attributes[k] = parse_date(v)

    def check(self):
        """ Check the validity of this task's attributes.

        Will raise an exception if any keys aren't valid python3 identifiers.

        Raises:
            ValueError: If any keys weren't valid python3 identifiers.
        """
        invalid = []
        for k in self.attributes:
            if not k.isidentifier():
                invalid.append(f'"{k}"')

        if invalid:
            invalid = ', '.join(invalid)
            raise ValueError(f'The following key names are invalid: {invalid}')

    @classmethod
    def createFromRst(cls, rst):
        """ Create a new Task from RST text

        The title is expected to be an RST level-1 heading (=====). This
        is followed by the task's description.

        At the end of the description are the attributes. These are single
        line attributes which contain metadata about the task.

        The minimum required set for these attributes are the task's ID,
        date of creation, username of the creator, tags, and assignee.

            ==========================
             PROJ-77: My task's title
            ==========================
            My tasks's description

            Other heading
            -------------
            My other heading description

            creator: ciminobo
            assignee: ciminobo
            creation_date: 05/07/1993
            ...

        Args:
            rst: RST-formatted text from which to create the task. This value
                be provided as a string of RST formatted text, a filename, or
                a list where each value represents a line of RST text.

        Returns:
            A new Task.

        Raises:
            ValueError: If the RST could not create a valid Task.
        """
        if type(rst) is str:
            rst = rst.strip().splitlines()
            if len(rst) == 1:
                with open(rst[0]) as f:
                    rst = f.read().strip().splitlines()

        if not rst:
            raise ValueError('The task was empty.')

        attributes = {}

        # Extract the attributes first. Some may be modified in special ways.
        curline = rst[-1].strip()
        while curline != '':
            curline = curline.split(':')
            key, value = curline[0], ':'.join(curline[1:]).strip()

            # Store tags as a list
            if key == 'tags':
                value = value.replace(',', ' ').replace(':', ' ').split()
                value = sorted(list(set(value)))
            elif 'date' in key:  # Try to parse dates
                value = parse_date(value)

            attributes[key] = value
            rst = rst[:-1]
            curline = rst[-1].strip()

        # Find the title.
        if re.search('^=+$', rst[0].strip()):
            rst = rst[1:]

        title = rst[0].strip()

        # Chop off the title block and build the description
        if re.search('^=+$', rst[1].strip()):
            rst = rst[2:]
        description = '\n'.join(rst).strip()

        return Task(title, description, attributes)

    def update(self, new_task):
        """ Update a task.

        The title and description of this task will be replaced, and the
        attributes will be replaced with the attributes in the new task.

        Designed to replace an existing task with the one modified in
        a text editor.

        Args:
            new_task: Other task instance whose attributes will be used.

        Raises:
            See createFromRst.
        """
        self.title = new_task.title
        self.description = new_task.description
        self.attributes.update(new_task.attributes)

    def getRst(self):
        """ Display this task in RST format.

        Returns:
            An RST string representing the content of this task.
        """
        s = []
        s.append('=' * (len(self.title) + 2))
        s.append(' ' + self.title)
        s.append(s[0])

        s.append(self.description)
        s.append('')

        # Add the attributes alphabetically
        for k in sorted(self.attributes.keys()):
            v = self.attributes[k]
            if k == 'tags':
                v = ', '.join(v)

            s.append(f'{k}: {v}')

        # Will become trailing newline
        s.append('')

        return '\n'.join(s)

    def __eq__(self, o):
        """ Returns true if o.id matches this one.
        """
        return self.id == o.id

    def __lt__(self, o):
        """ Returns true if o.id is less than this one.
        """
        return self.id < o.id

    def __getattr__(self, key):
        """ Expose keys in self.attributes as attributes.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            try:
                return self.attributes[key]
            except KeyError as e:
                raise AttributeError(f"'Task' object has no attribute {key}")
