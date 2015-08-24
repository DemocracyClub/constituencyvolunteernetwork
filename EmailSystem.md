# Introduction #

The new task email system is designed to ensure that emails can be confidently sent out knowing that they'll only be sent out to the right people and at the right interval and that automated welcome and reminder emails are handled.

# Steps #

## Creating emails ##

Task Emails are associated with a task and have a 'type' (welcome, reminder, oneoff). This type determines how the email queue handles it and with what priority. Welcome emails are automatically assigned on task assignment and sent once, reminder emails are assigned manually (should be automatic perhaps?) and sent once a week and oneoff emails are assigned manually and sent once.

## Assigning a task ##

To assign a task to volunteers use the usual interface at /tasks/admin/[n](n.md)/assign. Note that most tasks are now assigned on account activation.

When a task is assigned it automatically searches for a TaskEmail with Email Type of 'Welcome'. If it exists, it then assigns this email to the user. The email won't be sent until the email queue is flushed next.

## Assigning an email ##

Emails can also be assigned manually via /tasks/admin/[n](n.md)/assign/email, linked from the /tasks/admin page. This works in the same way to task assignment except you choose an email instead of a task. Emails are not sent until the email queue is flushed.

The pair (taskuser, taskemail) is unique i.e. a taskemail can only be assigned to a specific taskuser once.

## The email queue ##

To actually send an email ping /tasks/admin/queue. This will iterate for each user and find either the most recent unsent email (priority to welcome and oneoff, then reminder emails) or the reminder email sent the longest ago (so long as it was more than a week ago).

When the queue is run it outputs the emails it sent successfully.

## TODO ##

Reminder emails should probably be assigned on task assignment. They should also have an inbuilt taskuser status for which they're sent to. For example, you might want a reminder email to send to people who have started a task but not completed it.