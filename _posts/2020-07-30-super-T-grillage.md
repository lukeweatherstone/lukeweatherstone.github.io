---
layout: post
title: Creating a Super T bridge grillage model
subtitle: Each post also has a subtitle
gh-repo: lukeweatherstone
gh-badge: [star, fork, follow]
tags: [test]
comments: true
---
In Australia, Super T girders are a popular choice for building bridges. A Super T is a precast, prestressed concrete girder which is then combined with a reinforced concrete deck slab to make a composite structure. Super "T"s are named after their shape (and I think we really like them, hence the "Super").

I've been modelling a lot of Super T bridges lately so thought I'd collate my process in an article to solidify my understanding (you're welcome future Luke) and hopefully helping out any readers who are interested.

To illustrate this, I'll run through a recent example of a Super T road bridge. This particular bridge is two spans over a new roadway. The spans are similar length (although not exactly the same - we'll get to that).

The abutments are reinforced concrete headstocks sitting on reinforced concrete piles. The pier is a blade wall and is made integral with the deck by way of a cast-in-situ stitch pour after the girders are placed and deck is cast.

The bridge will carry two lanes of a local road and a shared path. The road will have one cross fall, the shared path will have another - they'll meet at the kerb. On each side, we'll have a precast Medium[^1] performance barrier with a stitch pour to tie it to the deck. It has zero skew.

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



[^1]: **Medium** performance level barriers are the highest level typical barrier referenced in Australian Bridge codes (currently AS 5100-2017). These barriers apply to bridges over rail lines, major waterways and major roads. Essentially all the high-risk bridges that are accessible to the public. Bridge barriers for say, mining vehicles, would require a separate assessment and get the performance class **Special**.

[hambly]: https://www.amazon.com/Bridge-Deck-Behaviour-C-Hambly/dp/0419172602