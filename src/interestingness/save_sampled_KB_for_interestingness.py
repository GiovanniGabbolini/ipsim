from src.knowledge_graph.io import save_sub_graphs as _save_sub_graphs
import pandas as pd
from src.data import data

"""
Saves a number of subgraphs for interestingness computation
"""


def save_sampled_KB_for_interestingness(n, start_from_batch=0):
    # Prepare data
    tracks = pd.read_csv(f"{data.raw_dataset_path}/spotify_recsys2018/tracks.csv", sep='\t', lineterminator='\r')
    tracks = tracks.sample(n*2, random_state=42)

    albums = pd.read_csv(f"{data.raw_dataset_path}/spotify_recsys2018/albums.csv", sep='\t', lineterminator='\r',)
    artists = pd.read_csv(f"{data.raw_dataset_path}/spotify_recsys2018/artists.csv", sep='\t', lineterminator='\r',)

    df = tracks.merge(albums, how='left').merge(artists, how='left')

    assert len(df) == n*2

    l = []
    for idx, row in df.iterrows():

        if type(row.track_uri) == str and type(row.track_name) == str and type(row.artist_name) == str and type(row.artist_uri) == str and type(row.album_name) == str and type(row.album_uri) == str:

            d = {
                'track_uri_spotify': row.track_uri,
                'track_name': row.track_name,
                'artist_name': row.artist_name,
                'artist_uri_spotify': row.artist_uri,
                'album_name': row.album_name,
                'album_uri_spotify': row.album_uri,
            }
            l.append(d)

            if len(l) == n:
                break

    if n > 1000:
        folder_name = 'sub_graphs_interestingness'
    else:
        folder_name = 'sub_graphs_interestingness_temp'

    _save_sub_graphs(l, start_from_batch=start_from_batch, folder_name=folder_name)


if __name__ == "__main__":
    save_sampled_KB_for_interestingness(20000)
