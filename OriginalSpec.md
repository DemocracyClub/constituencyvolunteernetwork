# [mySociety:public] A stand-alone coding task - looking for an	election volunteer system volunteer #

## Short Summary ##

ConstituencyVolunteersNetwork.org - A constituency based volunteering
system that people can sign up to in order to help mySociety and
TheStraightChoice.org in the run up to the next election.


## Fuller explanation ##

At the next election both mySociety and TheStraightChoice.org are
going to need a variety of tasks doing that are best done as widely
distributed volunteering tasks. These include:

  1. Getting people to scan and upload election leaflets
  1. Gathering candidate details in order to be able to email or post them the questions required for an election quiz (and yes, we know that Seb Bacon and Paul Youlten are working on parts of this, so we are hoping they'll leap on board this project with especial vigour).
  1. Publicising things like vote analyses in local papers around the country.
  1. Other stuff we haven't even thought of yet.

We therefore need a system that will let people say 'I'll become a
volunteer in my constituency', email them assigned tasks, record the
outputs of their tasks into a database, and make that data accessible
for end-user sites like the election quiz.


## Functional Spec ##

### Phase I. ###

Homepage should show map of the UK with constituencies filled in
different colours depending on whether anyone (or several anyones) has
volunteered in a particular constituency yet.

Homepage includes signup form for name, email and postcode (just like
HearFromYourMP.com really) , plus an explanation of what we're asking
people to sign up to. Signup should ask volunteers to consent to
having their email address CCed to other people who sign up in their
constituency, for low barrier connection between volunteers.

Signup involves email verification, but once done offers the chance to
volunteer for tasks in up to two other constituencies, as many people
have connections with more than one place.

In the first instance, this is all that needs to be done - the site
can start gathering volunteers before anything has been built beyond
this. It will be advertised prominently on TheyWorkForYou to get
traffic.

### Phase II. ###

Build system that allows admin to mail all volunteers to ask them to
gather MP candidates details. Emails should contain a unique link to a
page for their constituency(s) with a simple, usable form for adding
Name, Party, email, postal address, perhaps even photo. Each field
should be referenceable to an external website, or have an annotation
field where the user can explain where they got the info. The database
would then store any info they added, along with time and user
details. Volunteers would be able to login whenever they liked, using
the link in their email, to update and improve the data present. This
database could be pre-populated with Julian Todd's scraper code for
Wikipedia, which has already been able to get several hundred current
MP candidate names into structured data.

### Phase III. ###

Add feature so that admins can send arbitrary tasks out via email, and
have volunteers click links to indicate whether or not they did them,
for example uploading a leaflet to the StraightChoice, or asking
people to find local campaign groups that would contribute questions
to the election quiz (when that gets built).

Add feature so that if more than one person is signed up in a
constituency, they can communicate and work together easily.

### Phase IV. ###

Have huge election night party for 600+ volunteers  :)