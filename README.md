# The nofollow project

## Motivation 

RSS is one of the best things that ever happened for web users, not
just for information junkies but for those that wanted to keep an open
web and facilitate the flow of information.

Unfortunately for publishers, this ease of distribution meant also a
loss of control over the potential consumer base. With the adoption of
feed readers, publishers no longer had direct ways to measure their
audience.

One way found by publishers to mitigate this problem was to simply
provide an RSS feed with a small summary or introductory paragraph on
each entry, and a link at the end to the web site's "full html" page.

The "full html" meant tracking, invasive advertisements, heavy images,
unrelated links and all kinds of tricks to get you trapped into their
site, regardless of quality or care about the actual content.

Given that it started to become second-nature for me to open a link
from a RSS feed and instantly click the "Reader Mode" option of my
browser, I decided to write an application that could automate this
job for me: given a RSS feed, I would like to get all pages that the
entries were linking to and extract the readable content from them.
