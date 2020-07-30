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

The bridge will carry two lanes of a local road and a shared path. The road will have one cross fall, the shared path will have another - they'll meet at the kerb. On each side, we'll have a precast Medium[^1] performance barrier with a stitch pour to tie it to the deck.

### Setting up the grillage geometry
Before we get started, we need some more specifics, mainly from the road alignment team. Before we even start modelling, we need to do some calculations and digging to determine our geometry.

Picking up the phone, I find out the following:
~~~
B_road = 6          # clear width of the road carriageway, in metres
B_sup = 4           # clear width of the shared user path, in metres
B_barrier = 0.4     # distance from traffic barrier face to edge of deck, in metres
CF_road = 0.03      # cross fall for the road, as decimal
CF_sup = 0.025      # cross fall for the shared user path, as decimal
~~~

We can now determine the geometry of the deck

Here's an image!
![Super T](/assets/img/path.jpg)


[^1]: **Medium** performance level barriers are the highest level typical barrier referenced in Australian Bridge codes (currently AS 5100-2017). These barriers apply to bridges over rail lines, major waterways and major roads. Essentially all the high-risk bridges that are accessible to the public. Bridge barriers for say, mining vehicles, would require a separate assessment and get the performance class **Special**.