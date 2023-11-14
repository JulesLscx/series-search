import tools.unzipper
import os
import pandas as pd
from tools.tokenizer import Tokenizer, Lematize


def load_data():
    # Load all clean text
    PATH = os.path.join(os.getcwd(), 'data', 'processed')
    series = os.listdir(PATH)
    ser_name, sub_text = [], []
    df = pd.DataFrame(columns=['text', 'series'])
    for serie in series:
        path = os.path.join(PATH, serie)
        subs = os.listdir(path)
        text = ''
        for sub in subs:
            with open(os.path.join(path, sub), 'r', encoding='utf-8') as f:
                text += f.read()
        ser_name.append(serie)
        sub_text.append(text)
    df['text'] = sub_text
    df['series'] = ser_name
    return df


def test():
    tools.unzipper.rmtmp()
    unziper = tools.unzipper.Unzipper()
    unziper.u_zip("../keyword-generator-master/sous-titres.7z")
    unziper.categorise_all_sub(path_to_move='./data/processed')


if __name__ == '__main__':
    # test()
    df = load_data()
    df['text'] = Lematize().lematize_text(text_list=df['text'].tolist())
    print(df.head())
    exit(0)
