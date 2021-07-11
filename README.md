# IPSim

This is the official repository of [Giovanni Gabbolini](https://giovannigabbolini.github.io) and [Derek Bridge](http://www.cs.ucc.ie/~dgb/)'s paper "An Interpretable Music Similarity Measure Based on Path Interestingness".

It is possible to replicate all the results shown in the paper by running: `src/music_similarity/benchmark/paper.py`

## Installation

### Step 1

Create an environment with Python 3.7.3 and install dependencies by: `pip install -r requirements.txt`

### Step 2

Download the required data.
In particular, download and extract in the folder `res/r` the following data:

- Spotify's MPD: [https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge) ;
- _MIREX_ and _LastFM-g_: [https://zenodo.org/record/1291810#.X85HTC9Q1E9](https://zenodo.org/record/1291810#.X85HTC9Q1E9) ;
- _LastFM-h_: [https://grouplens.org/datasets/hetrec-2011/](https://grouplens.org/datasets/hetrec-2011/) ;
- _Facebook_: [https://github.com/nailson/lodrecsys15/tree/master/data](https://github.com/nailson/lodrecsys15/tree/master/data) ;

### Step 3

Prepare the required data by running: `config.py`.
