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
`cd code/submodules`, `git submodule update` and `pip install -e boris cindy kip` will install
the dependency packages in editable mode.

After that:

 - `django-admin migrate` to run the migrations
 - `django-admin createsuperuser` to get an admin account (follow the instructions)
 - `django-admin runserver 0.0.0.0:8000` will get the application running
 - (On another shell) `celery worker -A nofollow -B -l info` will start celery tasks and periodic tasks.

With everything running, you should be able to go to
http://192.168.23.15:8000/ and be redirected to the admin login
page. After logging in, you should be redirected to the home page, and
add either links or feeds.

### Installation

#### Warnings

 - **this section is certainly incomplete and assumes you are
experienced enough with deploying web services on the public
internet, as well as with the risks of doing so.**

 - This procedure assumes Ubuntu as the target Operating System. You
   may have to change some of the package names or install methods for other distros/OSes

 - If you have some ansible experience, the roles used might be a
   useful starting point for deploying on Ubuntu/Debian. PRs for expanding this are welcome.

 - PRs to get this deployed via docker are also _very_ encouraged.

 - This is assuming you are installing everything on the same
machine. While not recommended for any serious production deployment,
it should be okay for one single user. If you are looking for a more
robust deployment, you probably are experienced enough to want to
install things your own way. The only thing you will probably need to
know are the required environment variables, discussed below.

 - Please file bugs/get in touch for missing/wrong information.


#### Installing needed systems and servers

 - Postgresql: `sudo apt install postgresql-server libpq5-dev`
 - Rabbitmq: `sudo apt install rabbitmq-server`
 - [IPFS](https://docs.ipfs.io/introduction/install)
 - nginx: `sudo apt install nginx`
 - uwsgi: `sudo apt install uwsgi`


#### Setting up the web application
 1. Install python3 with the development header packages: `sudo apt install python3 python3-dev`
 1. Install virtualenv and pip: `sudo apt install python3-pip virtualenv`
 1. Create a python3 virtualenv
 1. On the virtualenv, install `pip install git+https://bitbucket.org/lullis/nofollow.git`
 1. Find the template file on
 `$REPO_ROOT/ansible/roles/templates/etc/nofollow.environment.j2` and
 save it on the host machine. Substitute all of the parameters inside
 double curly-brackets (`{{ }}`) with the proper parameters you'd like
 to set. (Be careful to set up long, random strings for the passwords and secrets)
 1. `set -a && source <environment config file>`


NGINX template file:

[Please use HTTPS](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04)

```
upstream webapp {
        server <your server name>:3031;
    }

server {
	listen 80;
	server_name <your server name>;
        return 302 https://$host$request_uri;
}


server {

	listen 443 ssl;
	server_name <your server name>;

        # configuration parameters for let's encrypt.
        # Take a look [here](https://gist.github.com/nrollr/9a39bb636a820fb97eec2ed85e473d38)

	root /var/www/html;

	location /static/ {
                alias <location of static folder (STATIC_ROOT), ending with slash>;
                autoindex on;
                expires max;
        }

        location /media/ {
                alias <location of media folder (MEDIA_ROOT), ending with slash>;
                autoindex on;
                expires max;
        }

        location / {
                include uwsgi_params;
                uwsgi_pass webapp;

                uwsgi_param Host $host;
                uwsgi_param X-Real-IP $remote_addr;
                uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
                uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;
        }

}
```


UWSGI template file:
```
base = <base folder>
home = <path to your virtualenv>
master = true
processes = 1
uid=<user running the application>
gid=www-data
protocol = uwsgi

socket = 0.0.0.0:3031

chdir = %(base)
mount = /=<path to your virtualenv>/lib/<python version>/site-packages/nofollow/wsgi.py
manage-script-name = true

vaccum = true
die-on-term = true

env = NOFOLLOW_DATABASE_ENGINE=django.db.backends.postgresql
env = NOFOLLOW_DATABASE_HOST=localhost
env = NOFOLLOW_DATABASE_NAME=<db_name>
env = NOFOLLOW_DATABASE_USER=<db_user>
env = NOFOLLOW_DATABASE_PASSWORD=<db password>
env = NOFOLLOW_BROKER_URL=<rabbitmq_url>
env = NOFOLLOW_BROKER_USE_SSL=0
env = NOFOLLOW_STATIC_ROOT=<path to folder of static files>
env = NOFOLLOW_SITE_LOG_FILE=<path to log file>
env = UWSGI_SOCKET=0.0.0.0:3031
env = UWSGI_MASTER=1
env = UWSGI_WORKERS=4
env = NOFOLLOW_SECRET_KEY=<your django secret key>
env = DJANGO_SETTINGS_MODULE=nofollow.settings
env = VIRTUAL_ENV=<path to your virtualenv>
```


TODO:

 - systemd for web application
 - systemd for celery workers


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
