agile = """\
################################################################################
# This is a configuration for projects intended to be managed using agile
# methodology. The settings in this file will be copied to the project in
# project.yaml
#
# Settings in this file that begin with a double underscore are automatically
# replaced when the real project configuration is created.
#

# Default zettel format
zettel_format: md

# Default headings for new tasks
headings: []

################################################################################
# Agile tasks have attributes geared toward agile practices.
#
# Estimate represents the effort a task will require to complete. This value
# should be estimated during backlog grooming sessions. A team may use various
# estimation techniques for this value. Some examples are points, t-shirt sizes,
# or simple time estimates.
#
# Value is meant to capture how much direct value a task adds to a project. This
# field could also be thought of as a task's priority. A development team may
# use numbers or words (high, medium, low, miniscule...) to describe this.
#
# A task's type should be either "story" or "epic" as basic starting values. An
# epic should have stories link to it, while stories should, in general, link to
# an epic. An epic might be something like a major release capturing stories
# necessary to the success of that release.
#
# Stage represents a task's progression. General values are "todo",
# "implementation", "testing", "review", and "closed".
#
# Resolution is meant to capture how a task was resolved. "completed" or
# "won't do" are basic ideas for this value.
#
attributes:
  assignee:
  sprint:
  estimate:
  project_name: __DEFAULT_PROJECT_NAME
  time_spent:
  resolution:
  stage: todo
  type: story
  value:

################################################################################
# Prefix of the titles of newly created tasks.
#
task_prefix: __DEFAULT_PREFIX
"""
