#Seb's version of a larger vision for Democracy Club

# Overview #

Democracy Club is, at its simplest, just a way to assign tasks to interested people.

There have been conversations about its main intended use as a task-assigning system: to get better coverage of the next election.  If this were in scope, I'd love to see it evolve into a resource for constituents to see the general election from a local perspective.

By focusing on **local** issues, the site will:

  * generate more interesting, less party-spun responses from candidates
  * stimulate debate about voting along candidate vs. party lines
  * hopefully give people a more interesting, relevant angle on the election
  * provide a resource which functions as a hub for hyperlocal websites: basically a link directory, but possibly with some simple tools to facilitate setting up new hyperlocal websites

# Functionality #

For a user, the site would work something like this:

  * a new visitor will enter their postcode and get taken to a page for their constituency
  * here they will see information that is aimed at helping them distinguish between individual candidates:
    * short biogs of each candidate, including a list of their main campaign platform, areas of speciality
    * a table showing some key issues and the candidates' views on these.  the questions would be a mixture of local and national, but mainly local
candidates would be asked to assign a level of importance to the issues
    * links to relevant information on TWFY about the incumbent
    * links to general party information (e.g. a crowdsourced, simplified version of each party manifesto -- see below)
    * a "who agrees with me" tool: order the issues by importance and "for" and "against" for each one, and match to the candidates
  * there will also be some general local / activist / general election information, in particular:
    * a list of local issues, with links to blogs as they exist; possibly cross-referencing to a Democracy Club tool that helps constituents interested in a particular issue to collaborate (e.g. a simple blog and a mailing list gets set up when more than 5 people express an interest in an issue without a local web presence)
    * a stream of tweets relevant to the constituency (identified by the intersection of a generic TWTWFY hashtag and the new twitter geolocation features (pending their full release and uptake))
    * a list of local news media and contacts
    * (possibly) for the general election itself, a dedicated geolocated twitter feed for gathering responses during polling and returning (or, if it's available by then a Google Wave for each constituency).  It would act as an online hub for talking about the election locally, as it unfolds.

The key tasks involved in building up this data will be completed using Democracy Club.

The tasks are:

  * Gather information about candidates.  We will ask specific information (name, contact details, party, etc).  When someone enters data they have to specify their source.  Once data has been entered it needs to be verified by one other volunteer, when it will be confirmed.  Confirmed data can be challenged at any point by any other volunteer.
    * Challenges will have to be confirmed by another, randomly picked volunteer.
  * Gather questions.  I believe the best way to stop partisan question-loading is to crowdsource what the most important local issues are.
    * We should probably ask Democracy Club volunteers to do an initial survey of local issues through web research, contacting local papers (identified using http://news.mysociety.org).
    * They would also take into account what each candidate themselves thought were the most important issues (and this would be available on the website).
    * Random site visitors can be asked to suggest other local issues.
    * DC volunteers would review all these issues.  There would be a polling mechanism on the constituency page to get a sense of what issues are considered important, but the volunteers get final say.
    * Confirmation of a volunteer's list of questions is carried out by a randomly picked volunteer from a nearby constituency.  The final list of questions should be phrased as statements with which the candidate can agree, disagree, or leave neutral (to aid matching candidate views to constituent views)

  * A small number of questions could be regarding national issues, but (a) these are less likely to get interesting responses from candidates, as they will toe the party line; (b) it's easy to find out the party line on these issues anyway.

> For national issues that we do want to include, in addition to what candidates think are the most important national issues to their constituents, these should also be retrieved from the party manifestos

  * To do this, we would create a tool to crowdsource compressing manifestos into a series of pledges.  (e.g. give someone a random manifesto paragraph and ask them to reduce anything that sounds like a pledge into something of less than 10 words)

  * Pose the questions & gather the answers.
    * To ensure we get interesting answers, it's been suggested we somehow make audio recordings and record them on the website.  If we did this, we could use a mixture of audiboo and skype.  The problem here is that it's quite a hurdle to jump in order to contribute.  Not only would the audio have to be recorded, but a shortened transcript would need to be created.
    * I wonder if, rather than this, a strategy of keeping the questions as hyper-local as possible (a) will make for more interesting answers even if the candidate refers to central press office; (b) gives the site it's really interesting angle: what if elections were really about candidates and local issues rather than national ones.
    * Candidates would be emailed or called for their views by local volunteers.  The issues would be phrased as "agree" or "disagree" but candidates would be allowed about 200 words to qualify their views.  They would also be asked to rank the issues in order of importance.  In the case of a personal interview, we would have to ask the DC volunteer to record and upload the primary data.  As outlined above, I wonder if it will be OK to do this by email / letter, which would reduce barriers to getting data in.
  * Write the "who agrees with me" tool, which could also plot you against other constituents