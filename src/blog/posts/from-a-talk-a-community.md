---
title: "From a talk, a community: The start of Satyrn AI"
date: 2026-09-29
authors:
  - pauleveritt
tags:
  - community
description: "The story of how Satyrn AI was born from a closing keynote at EuroPython, the community that formed, and what we hope to be."
---

On July 17 I gave the closing keynote at EuroPython. Today, on October 1st,
Python 3.15 ships. And our Satyrn AI community, born after that talk, delivers
(likely?) the only model on Earth that knows the new Python. This is the story
of how we started, who we are, and what we hope to be.

<!-- more -->

Here's the full talk:

<iframe width="560" height="315" src="https://www.youtube.com/embed/F7pc-YxxZAc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## The talk

The EuroPython organizers felt that Python developers have a lot of anxiety about what AI is doing: to
their careers, their craft, even to the world at large. And it's true! They asked me to give closing remarks
that would send them out of the conference with some energy, some hope.

At the PyTV event in Amsterdam, I talked with Carol and Georgi about this. We in Python have more power than we think
we do. What if we took our power back? Jupyter showed that a community-owned volunteer project could
ship an end-user application and become a force, and a force for good. What if Python could do that in AI?

I staffed the idea through the ongoing months, talking and listening with lots of folks, including at PyCon US. I asked
the conference organizers if I could launch something (and if I could use some colorful language at the end) and
got the ok.

But then it was the day.

Was I going to just talk in generalities? Or say the Satyrn name out loud and see who was in? I chatted with Reuven the
morning of the talk. He encouraged me to give it a shot.

So I did. I put up a slide, asked the audience to believe, and encouraged anybody interested to come
talk directly after. I said: let's do something crazy. We have just over 2 months. Let's ship a model supporting Python
3.15 when it is released. And this happened...the first 45.

![45 community members outside after the EuroPython keynote](../../assets/2026/from-a-talk-a-community/europython-afterparty.jpg)

Here's what I learned: it wasn't me, or the talk. Instead, there was a power already sitting inside everyone. Folks
aren't happy with what AI is doing to us and our community, and they want to do something.

## Immediate aftermath

So I went directly to vacation.

In hindsight, sure, not the best idea. Staying for the sprints would have been great to help build
the fighting-force. Which meant my vacation was a lot of Satyrn.

But it also meant a lot of people immediately sprang into action. The indispensable Pelle. The stars: Michał and
Laura. Daria, Emma, Zsófia, Nicola, Mike, Dom, Geoff, Lukasz, Koudai.

And very much: Carol, then Dawn.

We built a series of teams, got to work.

## The setback

I came into EuroPython thinking I was just a few days way from having a working Pi extension and eval harness. I was
wrong. Wronnnnnnggggg.

Nearly every day of vacation was me saying on Discord: "Today's the day." Then finding flaws after overnight runs
of the evals. I lost so much momentum and project enthusiasm as people waited for me to show my homework.
This went on until the 3rd week of September, perilously close to the October 1 deadline. Multiple "start overs."

Ultimately we have *something* for the Satyrn Engine (the Pi extension.) But the whole experience showed that the Satyrn
Evals harness was, at this point, more valuable. Ideas are now cheap, everybody can get their idea
generated. But the agent lies to you about your brilliant idea and it takes weeks of shooting holes in the bottom of
the boat before you realize, gotta start over with a new boat.

Evidence. That's all the matters. Start with the evidence of the
[small model pathologies](https://pauleveritt.github.io/satyrn-evals/pathologies/) and
make sure you know the actual problem. Then, experiment and make sure you have an actual solution,
in a reliable harness, at n=32 or more.

However, while I was cyclically failing, Michał had built a team that was creating the infrasture for fine tuning
and the training data not just for Python 3.15 but also 3.14 (as most small models don't cover that either.) Their
work is indeed the star of this first milestone, and possible the next milestone as well.

## What we hope for

- Go over the parts of the talk and the mission
- How we hope to work
- How we are different

## Where we are, what's next

This group of folks actually did something. In almost no time, they sprung into life, organized, learned,
and delivered something truly unique.

It's just a first start, and it's proof-of-concept-y. We're not claiming it's production ready.
But we have a model that knows Python, an engine that can help small models do medium work without going in the ditch,
and an eval harness that can help grow a community of harness engineers.

We have a website with a really lovely and purposeful design from Laura, plans for how to do education and onboarding
for these topics, ideas for how to organize all the smart ideas in Python using no-algorithm old-school web. And we have some tangibly-useful and innovative things cooking for the next milestone.

Most of all, we have a purpose. AI Our Way, from us, for us. We have an us.

## Gratitude

I think I can speak for all of us on the project about the deep gratitude we feel for this effort.
For Python itself and the world-wide community of super-cool, super-interesting folks that believe in the
common good, at a time when that's being overshadowed by a culture of shareholder value.

For an idea of AI Our Way, something we can believe in, something we can fight for, that was sitting there in the
forest, waiting to be discovered.

And most of all, for all the new friends we have that are crazy enough to try.

Hope is making a comeback.
