# The nofollow project

### Introduction - what is nofollow?

#### Self-hosted bookmark and read-it-later link formatter

nofollow is a self-hosted alternative for services that manage online
articles and make them more readable - like pocket and instapaper -
with a twist: after cleaning the extracted content from the page, it
saves the content (html and linked media) on [IPFS](https://ipfs.io).
This provides the ability to create some sort of distributed, curated
web archive, where each host is responsible for hosting only the links
they are interested in keeping around. No more link rot for your bookmarks.


#### *Real* Feed Syndication - no more summary-only feeds.

Another thing nofollow makes possible is to take RSS/Atom feeds that
provide only a summarized view and generate a new feed with the full
content of the entries. This allows you to read the content in your
favorite feed reader, any way you like it. This was the reason I
started this, by the way. It was getting very annoying to see feeds
with nothing but two lines of text and a link to the website, and I
wanted to take this power back to myself.


### Architecture

I am implementing this using Django, and celery for the handling of
all task processing. My intent is to keep this code as modular as
possible, meaning that all modules are implemented as django plugabble
apps, each on its own repository. This should make things easier for
those that want to contribute to specific parts of the project, or
that would like to have only certain functionality for their own
installs. If you are not interested in the IPFS part, for example, it
shouldn't be that hard to remove it.

A quick summary of the current modules, along with explanations for
the terrible puns that led to their names

 - [boris](https://bitbucket.org/lullis/django_boris) is the module
   that keeps track of links, crawled links and the implementation of
   the Spider class. [The Who](https://en.wikipedia.org/wiki/Boris_the_Spider)
   is to blame for this one.

 - [cindy](https://bitbucket.org/lullis/django_cindy) is the django app
   that creates new syndication feeds out of the summary-only feeds.

 - [kip](https://bitbucket.org/lullis/django_kip) is the module that
   provides IPFS models to manage IPFS content and links. This module
   also _keeps_ (wink, wink) the people-names-naming convention.



### Development

You need to have any reasonable recent version of vagrant and
ansible. Running `vagrant up` should create and provision a box with
an installed IPFS server, a PostgreSQL database as well as all the
dependencies needed to get the django and celery applications running.

During provisioning, the VM will have the 192.168.23.15 ip address,
and 4GB of memory available. If you want to use a different address,
or use more/less memory for the VM take a look at the Vagrantfile and
the environment variables that can be defined to override the default
parameters.

Ansible provision installs the versions on the pluggable apps (boris,
cindy, kip). For development, you will probably need to have the code
repository of the apps themselves. They can be installed as
submodules: on the _host_, you should be able to `git submodule
update` and get these repos on the 'modules' folder.

If everything goes well: you should be able to `vagrant ssh` to ssh
into the box and get to bash with an already-activated virtualenv.
`cd code/modules` and `pip install -e boris cindy kip` will install
the dependency packages in editable mode.

After that:

 - `django-admin migrate` to run the migrations
 - `django-admin runserver 0.0.0.0:8000` will get the application running
 - (On another shell) `celery worker -A nofollow -B -l info` will start celery tasks and periodic tasks.

### Installation

TODO


### Ideas/Things I would like to see implemented (in order of what I am inclined to work first):

 - [] Search
 - [] UX improvements: screenshots of crawled links, add notifications for events happening in the background (new feed update, link processing is completed, etc), styling of the readable page.
 - [] Federation: allow your instance to connect to others and share links.
 - [] Federated/distributed search:
 - [] Custom crawlers: at the moment, every crawled page gets its content extracted using the [readability](https://pypi.org/project/readability-lxml/) project. But the machinery is already there to allow for more custom, site-specific crawlers. E.g: let's say that you are the subscriber of a site with exclusive content. We can have a spider that authenticates to the website to get this exclusive content for you.
 - [] An easy "save in nofollow" bookmarklet.
 - [] Firefox/Chrome extensions that detect URLs already seen by
   nofollow and substitute the link for your nofollow server version
 - [] send to kindle
