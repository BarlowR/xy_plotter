# Project Proposal

## Overview & Motivations

I recently picked up a cheap clone of an [AxiDraw plotter](https://www.youtube.com/watch?v=5492ZjivAQ0&t=26s), and I've been playing around with it and exploring some of its capabilities. One cool application of these that I'd like to explore is plotting computer generative art; Matt Deslauriers has a fantastic writeup on the subject, along with some really good illustrations on his [blog](https://mattdesl.svbtle.com/pen-plotter-1). I'm particularly interested in the augmentation of human art by a set of algorithms to create something that's a mix of human and machine; I think there are some really cool drawings to be made in the intersection of the two spaces.

As a first step to start getting into generative art, I'd like to implement a front end design system for generating art to be drawn by my plotter. The initial functionality will be image intake and processing; I'd like to be able to import a raster image taken of a hand drawn design, and convert it into a vector format for manipulation and plotting. 

I  plan to write an implmentation of the alogrithm described in [this paper](http://potrace.sourceforge.net/potrace.pdf), and create a basic GUI for image intake and visualization of the resulting vector image files. Next I'll be building functionality for manipulation of the vector images, but I'm not sure how far I'll get with that in the next few weeks. 
