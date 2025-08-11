mdbSort README

CONTENTS
========

1.  Decription
2.  Data Organisation
3.  The Sort Schemes
4.  The Demo Programs
5.  Statistics
5.  Dependencies
6.  Notes & Observations
7.  License




1.  Description
---------------
This proof of concept and demonstration code is intended for academic and
research purposes only; it has no real practical use.

It demonstrates an algorithm for exchange sorting of data based around
organising the data to be sorted in conceptual multi-dimensional arrays.




2.  Data Organistion
--------------------
In most cases, a typical set of data to be sorted can be thought of as a
one-dimensional array:

Index    0    1    2    3
        ---- ---- ---- ----
       | d1 | d2 | d3 | d4 |
        ---- ---- ---- ----

In a Bubble sort, we compare each sort key with the next i.e. index n is
compared with index n+1 and if, depending on the sort order, the comparison
idicates that the two sort key values are in the 'wrong' order they are
exchanged.  In a Bubble sort then, we can think of the comparison as being
between neighbours within a single dimension.

Alternatively, we could reorganise the one-dimensional array of the sort
key values above into a two-dimensional array as below:

Index    0    1
        ---- ----
   0   | d1 | d2 |
        ---- ----
   1   | d3 | d4 |
        ---- ----

By doing this we now have up to two neighbours for each sort key value i.e.
data item d1's one-dimensional neighbour remains data item d2 but now it has
a two-dimensional neighbour in data item d3.

If we had more data we could add another dimension to the array, as shown
below in the dodgy ascii art diagram (The numbers are the data items and
not the key values themselves. Note data item d2 is hidden).


             / \
           /     \
         /    d6   \
       / \         / \
     /     \     /     \
   /    d5   \ /    d8   \
  |\         / \         /|
  |  \     /     \     /  |
  |    \ /    d7   \ /    |
  |  d5 |\         /|  d8 |
  |\    |  \     /  |    /|
  |  \  |    \ /    |  /  |
  |    \|  d7 |  d7 |/    |
  |  d1 |\    |    /|  d4 |
   \    |  \  |  /  |    /
     \  |    \|/    |  /
       \|  d3 |  d3 |/
         \    |    /
           \  |  /
             \|/


Now, instead of d1 having neighbours in just two dimensions; d2 & d3, we
have neighbours in three dimensions: d2, d3 & d5 respectively, as we move
up the dimensions, with which we can compare values.

However, the problem with actually orgainsing the data to be sorted in
this way means that only the lowest 'corner' item i.e. index 0/d1, gets the
full range of dimensional neighbours with which to compare whereas d3, for
example, has no higher two-dimensional neighbour, even though it does have a
higher three-dimensional neighbour in d7.

To get around this, and to also remove the need to transform the data in to
what can quickly become very complex multi-dimensional arrays (1,000,000
items would need an array with 20 dimensions) a series of offsets
can be used instead and this not only removes the need to transform the
data but also means that every item has a full virtual or conceptual multi-
dimensional stack above it.

Using the example above, of eight values to be sorted, we'd need an offset
series of 1, 2 & 4 so that d1(index 0) would still be compared with
d2(index 1 == index 0 + 1), d3(index 2 == index 0 + 2 & d5(index 4 ==
index 0 + 4).

Now though, d3(index 2) can be compared with d4(index 3 = index 2 + 1),
d5(index 4 == index 2 + 2) & d7(index 6 == index 2 + 4).




3.  The Sort Schemes
--------------------
Included with this demo are three different sort schemes named 'basic',
'modified' & 'bug'.

Each scheme starts by comparing at the highest possible dimension and drops
down through the dimensions until an exchange occurs but then differ in what
they do after an exchange has been made.

The 'basic' scheme
------------------
Once an exchange has been made with the 'basic' sort scheme the sort returns
to the next item in the data and starts a new set of comparisons, starting
once again with the highest possible dimension and working its way down
until it is either exchanged or no exhanges are found.

The 'modified' scheme
---------------------
In the modified scheme, after an exchange has occurred, further comparisons
are made at lower dimensions, but with the new neighbouring data items,
until we end up comparing with its 1-dimensional neighbour.

The 'bug' scheme
----------------
This is probably the most interesting of the schemes included and is the
result of a bug in the original iteration of the modified scheme, hence
its name.  It has been included, however, because it appears to be the
most efficient, by quite some way, of the three included schemes.

The bug that lead to this scheme (an omission of setting a loop exit flag)
meant that after an exchange had been made, then instead of moving on to the
next item of data and restarting at the top of the dimensional stack, the
sort engine continued to drop further down the stack of dimensions, making
further comparisons until it reached the lowest dimension.  However, the
subsequent comparisons are not made against the original data item but with
the exchanged item.

At least, that's how the schemes are intended to work.




4.  The Demo Programs
---------------------
All four of the included programs use the optparser module for parameter
handling; calling any of the programs with either the '-h' or '--help'
params will provide a short help listing.  In addition, the Demo1 & Demo2
programs use the pyGame module to display their graphical output.




mdbSortDemo1.py
---------------
This program displays the progress of the sort process using the diagonal
line format and really needs to be called with either the '-I' + '-W' or '-p'
params to introduce, respectively, a short interval or a prompt between
sort passes to be able to actually see what's going on.  The size of the
window will be equal to the number of sort values i.e. specifying 1000
sort values will result in a 1000x1000 window.  The '-W' param
keeps the final result window open for the specified number of seconds
before it is closed.  If the '-p' param is used then the window will close
after acknowledging the final prompt.

Usage: mdbSortDemo1.py [options]

Options:
  -h, --help            show this help message and exit
  -a, --ascending       Sort to ascending order [True]
  -d, --descending      Sort to descending order [False]
  -D, --doubleSort      Sort ascending then descending [False]
  -i string, --initialOrder=string
                        Initial Order of data (random/reverse) [random]
  -I n, --interval=n    interval in seconds between sort passes [0]
  -l n, --keyLength=n   Key Length [8]
  -m n, --maxDimensions=n
                        Maximum num of dims when testing
  -n n, --numElements=n
                        Number of elements to sort [200]
  -p, --prompt          prompt to continue between sort passes [False]
  -s string, --scheme=string
                        Sort scheme (basic/bug/modified) [bug]
  -S, --stable          Make the sort stable by adding a secondary key [False]
  -W n, --wait=n        Wait (sleep) seconds after finish [0]

Example:

  mdbSortDemo1.py -n 1000 -W 2 -I 2

    -n 1000         Generate 1000 data items in random order and sort them
                    in to ascending order.

    -W 2            Keep the display window open for 2 seconds after the sort
                    has completed.

    -I 2            Pause for 2 seconds between sort passes.




mdbSortDemo2.py
---------------
This program displays the progress of the sort process as a 2-d array,
oriented top-left to bottom-right, where the value of the sort keys are
colour-coded and the entire window area is used.  However, in order to
produce an output that was easily interpretable meant using a limited
pallette of colours which, in turn, meant using a limited range of sort
key values.  Thus, the the test data that is generated to be sorted
will contain many duplicate values (Note the '-S & --stable' params).
The '-I' + '-W' or '-p' params have the same meaning as used in the
Demo1 program.  However, because the full window area is used to plot
the data the size of the window will instead be the square root of the
number of sort values and not equal to it i.e. specifying 1000000 sort
values will result in a 1000x1000 window.  Because the Demo2 program will
typically be run with a far greater number of sort values and thus take
longer between sort passes, the '-I' and '-p' params have less utility.
Using the '-W' parameter is still recomended to prevent the display
window closing as soon as the sort is finished.

Usage: mdbSortDemo2.py [options]

Options:
  -h, --help            show this help message and exit
  -a, --ascending       Sort to ascending order [True]
  -d, --descending      Sort to descending order [False]
  -D, --doubleSort      Sort ascending then descending [False]
  -i string, --initialOrder=string
                        Initial Order of data (random/reverse) [random]
  -I n, --interval=n    interval in seconds between sort passes [0]
  -l n, --keyLength=n   Key Length [8]
  -m n, --maxDimensions=n
                        Maximum num of dims when testing
  -n n, --numElements=n
                        Number of elements to sort [40000]
  -p, --prompt          prompt to continue between sort passes [False]
  -s string, --scheme=string
                        Sort scheme (basic/bug/modified) [bug]
  -S, --stable          Make the sort stable by adding a secondary key [False]
  -W n, --wait=n        Wait (sleep) seconds after finish [0]

Example:

  mdbSortDemo2.py -n 1000000 -W 2 -D -s modified -S

    -n 1000000      Generate 1000000 data items in random order and sort them
                    in to ascending order.

    -W 2            Keep the display window open for 2 seconds after the sort
                    has completed.

    -D              Perform a double-sort i.e. sort ascending and then
                    Descending.

    -s modified     Use the 'modified' scheme instead of the default 'bug'
                    scheme.

    -S              Make the sort stable.




mdbSortDemoFile.py
------------------
The purpose of this program is to produce a sorted output file that may be
compared with a similarly sorted file (from the same input file) produced
by other sort programs to prove that the sort algorithms work (see also
mdbSortGenerateDataFile.py below).

Usage: mdbSortDemoFile.py [options]

Options:
  -h, --help            show this help message and exit
  -a, --ascending       Sort to ascending order [True]
  -d, --descending      Sort to descending order [False]
  -D, --doubleSort      Sort ascending then descending [False]
  -i str, --inputFile=str
                        Input File
  -l n, --keyLength=n   Key Length [10]
  -m n, --maxDimensions=n
                        Maximum num of dims when testing
  -o str, --outputFile=str
                        Output File (MUST NOT EXIST)
  -s str, --scheme=str  Sort scheme (basic/bug/modified) [basic]
  -S, --stable          Make the sort stable by adding a secondary key [False]
  -z, --statistics      Print statistics [False]

Example:

  mdbSortDemoFile.py -i foo.txt -o bar.srt -z

    -i foo.txt      The input file to be sorted.

    -o bar.txt      The output file of sorted data.  If this
                    file already exists the program will immediately exit
                    without overwriting it.

    -z              Print the iteration and cumulative sort statistics.




mdbSortGenerateDataFile.py
--------------------------
The purpose of this program is to produce a text file of data, in reverse
or random order, that may be used for input by the mdbSortDemoFile.py
program.  The data generated consists of integer numbers in the range 0 to
the number of elements specified, padded with leading zero '0' chars to
the length specified by the -l/--keyLength param [10 chars].


Usage: mdbSortGenerateDataFile.py [options]

Options:
  -h, --help            show this help message and exit
  -i str, --initialOrder=str
                        Initial Order of data (random/reverse) [random]
  -n n, --numElements=n
                        Number of elements to sort [1000000]
  -o str, --outputFile=str
                        File Name (MUST NOT EXIST)

Example:

  mdbSortGenerateDataFile.py -i reverse -n 10000 -o foo.txt

    -i              Generate the data in reverse order.

    -n 10000        Generate 10000 values.

    -o  foo.txt     Write the data to a file named 'foo.txt'.  If this
                    file already exists the program will immediately exit
                    without overwriting it.




5.  Statistics
--------------

The Demo1 & Demo2 programs output some statistics for each sort pass as
the sort progresses and then outputs the cumlative statics after the sort
has completed.  The statistics comprise a number of 'space' separated
columns of integer values as follows:

  Col 0:    Iteration

  Col 1:    Highest active dimension index (starting at 0)

  Col 2:    Total number of tests across all dimensions

Then follow a number of columns showing the number of exchanges that were
performed in each dimension of the sort, from the lowest dimension to the
highest.  Eaxmple iterative and cumulative statistics from a run of the
mdbSortDemo1.py program (specifying random initial data and 1000 elements
is shown below:

Iteration Statistics:
=====================
0 10 10700 1723 60 68 68 96 138 179 213 290 313 298
1 9 10836 1859 88 194 195 223 286 306 302 205 60 0
2 8 10294 1805 257 289 303 317 320 233 79 7 0 0
3 7 9257 1512 380 335 315 298 161 22 1 0 0 0
4 5 7594 721 297 220 158 41 5 0 0 0 0 0
5 3 5114 145 94 40 11 0 0 0 0 0 0 0
6 2 3010 17 13 4 0 0 0 0 0 0 0 0
7 1 1998 1 1 0 0 0 0 0 0 0 0 0
8 -1 999 0 0 0 0 0 0 0 0 0 0 0
=====================
Cumulative Statistics:
[8, 59802, 7783, 1190, 1150, 1050, 975, 910, 740, 595, 502, 373, 298]
=====================

The above shows that 11 dimensions (indexed 0-10) were used for this sort,
a total of 10700 tests were performed in the first sort pass and that the
number of exchanges that were performed in dimensions 0, 1, 2, 3, 4, 5, 6,
7, 8, 9, 10 were, respectively, 1723, 60, 68, 68, 96, 138, 179, 213, 290,
313 298.




6.  Dependencies
----------------
These programs import a number of python modules as lised below:

  os, sys, datetime, random, time, optparse, pygame




7.  Notes & Observations
------------------------

Origin
Behaviour
Worst case Scenario
Parallel processing
Sign off

Origin
------
I am not a Sort scientist and these mdbSort programs are the result of
something I noticed while playing with some simple algrorithms for
moving pixels about, depending upon their neighbouring pixels, in small 2-d
graphics regions.  What I noticed, as I watched the pixels move about the
display window, was that one of the algorithms that I had come up with was
actually performing a 2-dimensional bubble sort.  This distracted me from
my original line of idle curiousity and I ended up quickly writing some
simple proof-of-concept programs (in Python2 - this was late August 2009)
to check that it worked for 2, 3, 4 & 5 dimensions.

I then pretty much forgot about it until April 2012, when something must
have inspired me to write a more capable and polished version that could use
as many dimensions as were needed and which might give me more insight.
This resulted in the first version of the set of programs presented here,
albeit still in Python2.

I then forgot about it again, until May 2024, when I finally got around to
porting it to Python3, and when it occurred to me that other people might
find some aspects of the algorithm interesting.  Since then I've really
just been working on this documentation - always the hardest part.


Behaviour
---------
The essence of this sort algorithm is that it tries to exchange the item
being tested with another that is as far away (in the direction of the
sort) as possible, progressively reducing that distance until an
exchange is acheived (it should be noted that this is likely to result in
many 'overshoots', where an item is actually moved far beyond where it
should finally end up.  For example, consider a list of many items starting
with sort keys of '3', '1'... and that the inital highest dimensional test
hits a '2'; the '3', which was already close to where it should have been
will thus be moved a considerable distance away from where it was and will
need to be moved back during subsequent sort passes.  Also note that this
'overshoot' effect is worsened when the modified or bug schemes are used.

A more positive aspect of this sort algorithm is that it quickly (in terms
of sort passes) sorts the entire list into a 'roughly' sorted state, each
subsequent pass refining the 'quality' of the sort state.  This is perhaps
best seen with the mdbSortDemo2.py program where, with 1000000 items in
random initial order, all of the data appears to be in the correct 'half'
of the list and is semi-sorted within each half after the very first pass.
Subsequent passes refine the sorted state and by the fourth or fifth pass,
to the un-aided eye, the data 'looks' sorted (most people are unable to
to spot a single bit difference between two 24 bit RGB colour values).

Thus, the sort algorithm can be thought of as being very 'busy' during the
early sort passes, when the higher dimensional tests are available (as can
be seen in the iterative statistics).  However, as the data becomes 'more'
sorted, the the higher dimensional tests progessively become redundent
and the sort has to drop to lower dimensional tests, eventually resorting
to a simple 1-d bubble sort.  Obviously, as the sort progresses and fewer
dimensions can be tested, each pass performs fewer tests so requires less
time.


Worst case scenario
-------------------
Although based upon the simple 'bubble' sort algorithm I have no idea how to
work out the worst case scenario for this modified version of it because, to
me, it essentially seems to be chaotic.  Having run the programs many times,
especially the mdbSortDemo2.py program, typically with 1000000 values, there
seems to be little variation in the number of sort passess or the time
needed for the sort.  Neither the initial order of the data (random or
reverse) nor whether the sort is made stable seems to make much difference.


Parallel processing
-------------------
Although I believe that some degree of parallel processing is possible I
think it would need to be carefully controlled to avoid collisions as the
sort resorts to lower dimensional tests.  Apart from that, I've not
thought much more about it.


Sign off
--------
As stated at the beginning of this doc, this software is intended for
academic and research purposes and as such I have no desire or intention to
develop it any further; I have a few other half-finished idle-curiousity
projects I need to sort out, plus a couple of new ones I want to start.

Having said that, I'll attempt to find some time to apply any corrections
that anyone might find.  Although I believe I remember the sort algorithm
well and will be happy to discuss that, there's been a gap of about 13 years
between writing the code and writing this doc, so I'm not exactly familiar
with it anymore.

Regarding the code, I did make a decision to try to make the code 'obvious'
rather than 'clever' or 'Pythonesque'.  While there are some comments in the
code they were there mostly to remind myself of what was going on.

Ultimately,this code was written just to test and demonstrate an idea and
in itself isn't important.

Of course, Python certainly isn't the best language for this kind of task so
I would be very interested to hear from anyone who codes the algorithm in a
more sensible language.  I'd also be very interested to hear from anyone
who has a go at parellelising it.


License
=======
This work is published under the terms of the GPL V2 license, a copy of
which in included in the file GPLV2.txt

