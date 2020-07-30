---
layout: post
title: Creating a Super T bridge grillage model
subtitle: A worked example of a two-span integral bridge
gh-repo: lukeweatherstone
gh-badge: [star, fork, follow]
tags: [bridge design]
comments: true
---
In Australia, Super T girders are a popular choice for building bridges. A Super T is a precast, prestressed concrete girder which is then combined with a reinforced concrete deck slab to make a composite structure. Super "T"s are named after their shape (and I think we really like them, hence the "Super").

I've been modelling a lot of Super T bridges lately so thought I'd collate my process in an article to solidify my understanding (you're welcome future Luke) and hopefully helping out any readers who are interested.

### The example we're working with

To illustrate this, I'll run through a recent example of a Super T road bridge. This particular bridge is two spans over a new roadway. The spans are similar length (although not exactly the same - we'll get to that).

The abutments are reinforced concrete headstocks sitting on reinforced concrete piles. The pier is a blade wall and is made integral with the deck by way of a cast-in-situ stitch pour after the girders are placed and deck is cast.

The bridge will carry two lanes of a local road and a shared path. The road will have one cross fall, the shared path will have another - they'll meet at the kerb. On each side, we'll have a precast Medium[^1] performance barrier with a stitch pour to tie it to the deck. It has zero skew.

Because we're using Super Ts, and because we have an integral stitch pour, the construction staging is critical to the correct design of this bridge. Here, we're only looking at the actions on the bridge in its **final** configuration - that is, once it is open for design traffic. Other configurations will need to be considered separately.[^2]

### Setting up the grillage geometry
#### Lateral geometry
Before we get started, we need some more specifics, mainly from the road alignment team. Before we even start modelling, we need to do some calculations and digging to determine our geometry.

Picking up the phone, I find out the following:
~~~
B_road = 6          # clear width of the road carriageway, in metres
B_sup = 4           # clear width of the shared user path, in metres
B_barrier = 0.4     # distance from traffic barrier face to edge of deck, in metres
CF_road = 0.03      # cross fall for the road, as decimal
CF_sup = 0.025      # cross fall for the shared user path, as decimal
~~~

Taking into account the cross falls, we can determine the overall bridge width
~~~
import numpy as np

B_road_total = (B_road + B_barrier) / np.cos(np.atan(CF_road))
B_sup_total = (B_sup + B_barrier) / np.cos(np.atan(CF_sup))
B_total = B_road_total + B_sup_total

>>> B_total
10.804
~~~

Now making some choices on the number of girders for each portion of the bridge, and the space between each girder, we can get lateral coordinates for each girder.

Note that we want to explicitly define the number of girders for **both** the road portion and shared path portion because there are two different cross falls. This means we'd like to place the girders at that same cross fall, and as such the girder spacings under each portion will be slightly different.
~~~
gap = 30        # gap between each girder
n_road = 3      # number of girders for the road bridge
n_sup = 2       # number of girders for the shared path
~~~

Now calculating the girder flange width and spacing of the girders:
~~~
# Note that we'll minus half a girder here because the two bridges sides will "share" a gap between each girder.
flange_road = ((B_road_total * 1000) - ((n_road - 0.5) * gap)) / n_road
flange_sup = ((B_sup_total * 1000) - ((n_sup - 0.5) * gap)) / n_sup

space_road = flange_road + gap
space_sup = flange_sup + gap

>>> flange_road, flange_sup
2109, 2178
~~~

It's important to check that our flange widths are within range of what we'd expect for a Super T. Precast manufacturers typically have a minimum and maximum range they can go to, so we want to make sure this number is sensible. Here, we get values of `2109` and `2178` which are right about where we'd want them.

That all makes sense in code, but really, a table would help us to visualise what's going on. The fact that our bridge has 0 skew also makes things nice and simple. Here's one I prepared earlier:

| Element | Z coordinate |
| :------ | :------ |
| Edge 1 | 0 |
| Girder 1 | 1.089 |
| Girder 2 | 3.297 |
| Girder 3 | 5.471 |
| Girder 4 | 7.610 |
| Girder 5 | 9.749 |
| Edge 2 | 10.804 |


#### Longitudinal geometry
Going back to my phone conversation from earlier, we need the span lengths.
~~~
L1 = 30         # length of span 1 in metres
L2 = 33         # length of span 2 in metres
~~~

Now that we have the span lengths, we need to determine an appropriate spacing for the transverse grillage members. This part is trickier than before. Whereas previously we were modelling the **actual** positions of the girders, now we are idealising a continuous slab into a series of discrete beam elements.

Fortunately, Hambly, in [his book _Bridge Deck Behaviour_][hambly] (affectionately referred to as "The Bible" by many of my colleagues) has some guidance for us:
> The spacing of transverse members should be sufficiently small for loads distributed along longitudinal members to be represented with reasonable accuracy by a number of point loads, i.e. spacing less than about 1/4 of the effective span. In regions of sudden change such as over an internal support, a closer spacing is necessary.

He then goes on to say:
> The transverse and longitudinal member spacings should be reasonably similar to permit sensible statical distribution of loads.

So basically our elements should have a spacing of less than about 7.5 m (0.25 * 30), be roughly equivalent to the longitudinal girder spacing (approximately 2.1 m) and have a closer spacing over regions of sudden change (our integral pier).

We want numbers to the nearest mm for our spacings, so we'll go ahead and adopt the following:
~~~
sp_trans1 = 2               # transverse spacing of elements for span 1, in metres
sp_trans2 = 2.2             # transverse spacing of elements for span 2, in metres

n_trans1 = L1 / sp_trans1   # number of spaces created (should be an integer)
n_trans2 = L2 / sp_trans2

>>> n_trans1, n_trans2
15, 15
~~~

We're not too concerned with the detail over the support, so we'll keep these spacings consistent for each of the spans.

With the above properties in mind, we can now input the grillage elements to your finite element analysis program of choice. (For what it's worth, I'm using SPACE GASS here)
![Plan view of grillage members](/assets/img/grillage_plan.png)

A few things to note in the above. The green elements are the longitudinal members (our composite Super T girders). The blue elements are the transverse members (our slab). The pink elements are the edge of the deck - these will have a negligible stiffness, but we need them for load application. The red elements represent the cross girders and integral stitch.

#### We're not quite done yet
While we have all of our main elements input, we can be a little more exact and give this bridge some more capacity. To do this, we're going to add some stiff outriggers.

We'll get to sizing the Super T girders shortly, but at the moment, our idealised cross section looks something like this:
![Idealised grillage cross section - simple](/assets/img/grillage_cs_simple.png)

The green circles are a beam element with properties for the composite girder. The blue lines are the transverse slab elements. The problem here is the slab. It's spanning between the girder centroid, but really, it is supported by the girder webs.

Here we'll add our stiff outriggers, shown in orange:


[^1]: **Medium** performance level barriers are the highest level typical barrier referenced in Australian Bridge codes (currently AS 5100-2017). These barriers apply to bridges over rail lines, major waterways and major roads. Essentially all the high-risk bridges that are accessible to the public. Bridge barriers for say, mining vehicles, would require a separate assessment and get the performance class **Special**.

[^2]: For the sake of completeness, here's what I'm thinking the construction staging for this bridge would look like:  
    1. Carry out excavations
    2. Construct piled fondations
    3. Construct pier foundation, pier blade wall, abutment headstock and wingwalls
    4. Construct backfill and drainage system behind abutments to the underside of the approach slab level
    5. Construct falsework towers for temporary girder support at pier
    6. Erect girders onto bearings at abutments and temporary falsework towers/support brackets at pier
    7. Cast cross girders at abutments
    8. Cast main deck slab from abutment to within 2.5 m of pier centreline
    9. Cast integral stitch over pier
    10. Construct footway slab and kerb
    11. Construct approach slab and barriers
    12. Install approach pavements and surfacing on bridge deck

[hambly]: https://www.amazon.com/Bridge-Deck-Behaviour-C-Hambly/dp/0419172602