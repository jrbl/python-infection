What This Is
------------
This is an exercise intended to satisfy Khan Academy's take-home test. If you
this by googling their take-home test, shame on you! Do your own homework.

Cf. SPEC.txt for full details.

Running The Tests
-----------------
Simply run, "make test" to run all of the tests.

What I Want TODO Next
---------------------
I'd really love to hook some visualization up to Population(). I'm imaginging prefuse-style
spring model ball-and-edge graphs showing how users are connected to one another, and 
color coding users as the feature spreads among them. I suspect doing a good job on this
front end would take about the same time I've put into this back end. So if I do it, it'll 
just be for fun.

I'd also really like to make support for multiple feature infections explicit throughout.
It seems really artificial that you only be able to select across the graph one feature
at a time, and it would be nice to use Population.randomize() to create big, statistically
plausible user test sets that put people into multiple overlapping or orthogonal 
conditions.

