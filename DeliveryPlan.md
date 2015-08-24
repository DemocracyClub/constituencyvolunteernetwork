There's about 30 person days work here.  It needs to be done by 25 March, when it's speculated the next election might be (latest is June 3rd).  As of 11 Dec, there are about 60 working days until then.

# Complete the task framework #
As far as I can see, this means:

  * Finesse the UI
  * Set up emails to go out to people when tasks are assigned
    * Each task should have a URL; the URL in the email should go through to the DC website,  and if it's a "start" action, then we should redirect straight to the task URL.

**Effort estimate**: 2 days

# Getting better coverage #

We're aiming here to get at least two people in each constituency.

  * Add volunteer recruitment banner on MP pages in TWFY
  * Add similar banner to the conversion pages in WTT and FMS
  * Create a Task which is "sign up as many more people as possible, optionally bearing in mind this list of constituencies with no-one in them"
**Effort estimate**: 1 day
  * Create another task which is "hunt down people in these missing constituencies"
    * We can suggest they contact a local paper and ask it to run a feature, or find a blog of a political person in that constituency and contact them directly, or find local yahoo groups and email them
    * Task would be assigned to all volunteers; the task page would suggest a random constituency to tackle when logged in
**Effort estimate**: 1 day


# Gathering local issues #

  * Design a UI for gathering as many local issues as possible
    * A text input of no more than 8 words for the issue, optional 20 word expansion, mandatory "source" field (e.g. a blog or newspaper article)
    * Some kind of post-moderation feature such as "report this as inappropriate"
    * Once we add the ability for people to post content, we should probably add a captcha to the signup?
**Effort estimate**: 4 days
  * If we need more issues, consider setting a task to publicise the page in local media; print out posters; etc
**Effort estimate**: 1 day
  * When we have a decent number of local issues in a constituency (20?), we need to weed them down and improve them
    * Consider setting a task for each volunteer to review a randomly chosen set of issues in a constituency.  They would check the sources to make sure they are issues.
    * Consider a kittenwar-style interface for constituents to rank the issues; then we pick the top 5 (or so)
**Effort estimate**: 3 days

# Gathering local candidate information #
  * Screenscrape known sources of data
**Effort estimate**: 1 day
  * Set up UI for volunteers to edit, view, moderate existing and new data: name**, party**, email**, postal address**, website URL, plus find any candidates that we don't have, selection information, selection date, selection coverage, photo
**Effort estimate**: 4 days
  * Set task for volunteers to validate data we have and fill in holes, e.g. email candidate for photo
  * Set a task for volunteers to review and check
  * 11 working days before election, set a Task for volunteers to complete candidate info with late entries
**Effort estimate**: 1 day

Note: Some of this might be done by Edmund von der Burg at YourNextMP.com

# Making up a questionnaire #

  * Create UI and models for a questionnaire.  Questions will be phrased to allow them to be answered "yes/no/maybe" answers, plus a maximum of 30 words free text.  There must be a form that allows volunteers to build the questionnaire.  At this stage, we don't need to build the survey tool itself.
**Effort estimate**: 4 days
  * Set a task to turn issues into questions
  * When complete, set a task to check a random questionnaire form
  * mySociety will build into TWFY:
    * MP survey tool
    * constituent quiz tool
**Effort estimate**: 6 days

# Chasing candidates to take survey #

  * Send email to all candidates to take survey
  * Some time later, set a task to send a printed letter asking them to take survey (possibly we'll do this ourselves)
  * Set task for volunteers to personally chase candidates to take the survey

**Effort estimate**: 1 day

# Facebook application #

  * Make Facebook application that uses candidate data to allow a user to declare in their friends' newsfeeds one of the following
    * Undecided
    * Decided on a particular candidate/party (I think we should emphasize the candidate over the party, in line with our overall concept of candidate information?)
    * Decided to spoil the vote for a particular reason (with link to notapathetic.com)
    * Decided but not revealing (with appropriate explanation of the right to a secret ballot)
  * Use this to push Democracy Club information out to everyone, tell people about the survey, get more members, etc.

**Effort estimate**: 7 days, depending on state of Facebook API
**Depends on**: Candidate data, survey