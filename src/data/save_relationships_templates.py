import requests
from bs4 import BeautifulSoup
import re
import pprint
import json
from src.data.data import preprocessed_dataset_path


def save_relationships_templates():
    relationships = ['artist-work', 'artist-event', 'artist-label', 'artist-artist',
                     'artist-place', 'artist-recording', 'artist-release', 'artist-release-group']
    d = {}
    for r in relationships:
        d[r] = {}
        req = requests.get(f"https://musicbrainz.org/relationships/{r.replace('release-group', 'release_group')}")
        soup = BeautifulSoup(req.text, "html.parser")
        rels = soup.find_all("div", {'class': 'reldetails'})
        for rel in rels:
            t = rel(text='Long link phrase:')
            assert len(t) == 1
            long_link_phrase = t[0].parent.nextSibling.nextSibling.nextSibling
            long_link_phrase_p = re.sub(r"{([a-z]+):%\|([a-z]+)}", r"\2", long_link_phrase)
            long_link_phrase_p = re.sub(r"{.+?}", "", long_link_phrase_p)
            long_link_phrase_p = long_link_phrase_p.replace('is/was', 'is')
            long_link_phrase_p = long_link_phrase_p.replace('does/did', 'does')
            long_link_phrase_p = re.sub(r"performed$", "performed in", long_link_phrase_p)

            long_link_phrase_p = " ".join(long_link_phrase_p.split())
            long_link_phrase_p = long_link_phrase_p.strip()

            t = rel(text='UUID:')
            assert len(t) == 1
            UUID = t[0].parent.nextSibling.nextSibling.nextSibling

            if UUID == 'f8673e29-02a5-47b7-af61-dd4519328dd0':
                long_link_phrase_p = 'performed in'
            elif UUID == '3b6616c5-88ba-4341-b4ee-81ce1e6d7ebb':
                long_link_phrase_p = 'performed as orchestra in'
            elif UUID == '45115945-597e-4cb9-852f-4e6ba583fcc8':
                long_link_phrase_p = 'performed as chorus master on'
            elif UUID == '91109adb-a5a3-47b1-99bf-06f88130e875':
                long_link_phrase_p = 'remixed'
            elif UUID == '1ef6f500-d098-4768-ad00-72cc2bc2912f' or UUID == '601fc03e-1058-4ee6-a546-b914d55aa6ba':
                long_link_phrase_p = 'appears on the video of'
            elif UUID == '578ee04d-3227-4335-ba2c-11e8ba420e0b':
                long_link_phrase_p = 'directed the video of'
            elif UUID == 'b367fae0-c4b0-48b9-a40c-f3ae4c02cffc':
                long_link_phrase_p = 'produced'
            elif UUID == 'a7e408a1-8c64-4122-9ec2-906068955187':
                long_link_phrase_p = 'has video photography by'
            elif UUID == 'e74a40e7-0f27-4e05-bdbd-eb10f5309472':
                long_link_phrase_p = 'had a contract with'
            elif UUID == 'fe16f2bd-d324-435a-8076-bcf43b805bd9':
                long_link_phrase_p='has as personal label'

            pprint.pprint({'original': long_link_phrase, 'preprocessed': long_link_phrase_p, })
            print("\n")

            assert UUID not in d
            d[r][UUID] = {'original': long_link_phrase, 'preprocessed': long_link_phrase_p}

    with open(f"{preprocessed_dataset_path}/textual_templates_artist_relationships.json", 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    save_relationships_templates()
