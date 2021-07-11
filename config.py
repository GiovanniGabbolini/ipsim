from src.interestingness.save_sampled_KB_for_interestingness import save_sampled_KB_for_interestingness
from src.interestingness.interestingness_GB import save_count_sample
from src.music_similarity.dataset import prepare_facebook_recommender_dataset, prepare_lastfm_recommender_dataset, prepare_mirex_lastfmapi_dataset, save_dataset

# print("Saving sample KG for interestingness ...")
# save_sampled_KB_for_interestingness(20000)

# print("Saving interestingness ...")
# save_count_sample()

print("Preparing datasets ...")

prepare_mirex_lastfmapi_dataset('mirex')
prepare_mirex_lastfmapi_dataset('lastfmapi')
prepare_facebook_recommender_dataset()
prepare_lastfm_recommender_dataset()

save_dataset('mirex')
save_dataset('lastfmapi')
save_dataset('facebookrecommender')
save_dataset('lastfmrecommender')