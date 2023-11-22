import tools.unzipper
import os
import pandas as pd
from tqdm import tqdm
from tools.preprocessing import preprocess, StopWords


def load_data():
    # Load all clean text
    PATH = os.path.join(os.getcwd(), 'data', 'processed')
    series = os.listdir(PATH)
    ser_name, sub_text, episode_name = [], [],[]
    df = pd.DataFrame(columns=['serie', 'episode', "subtitle"])
    for serie in tqdm(series):
        path = os.path.join(PATH, serie)
        subs = os.listdir(path)
        text = ''
        for sub in subs:
            with open(os.path.join(path, sub), 'r', encoding='utf-8') as f:
                sub_text.append(f.read())
                ser_name.append(serie)
                episode_name.append(sub[:-4])
    df['subtitle'] = sub_text
    df['serie'] = ser_name
    df['episode'] = episode_name
    return df

def get_preprocessed_data():
    df = load_data()
    tqdm.pandas()
    print("Preprocessing data...")
    df['subtitle'] = df['subtitle'].progress_apply(preprocess)
    print("\033c")
    print("Preprocessing data, Done !")
    return df
