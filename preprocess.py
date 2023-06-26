import pandas as pd
from pathlib import Path

import click

# from utils.select_author import select_author_name
from utils.text_clean import text_cleanse_df

DATA_DIR = 'data/src/'
OUTPUT_DIR = 'data/out/'

WRITE_TITLE = False  # 2カラム目に作品名を入れるか
WRITE_HEADER = False  # 1行目をカラム名にするか（カラム名「text」「title」）
SAVE_UTF8_ORG = True  # 元データをUTF-8にしたテキストファイルを保存するか


def make_ziplist(author_id):
    tx_dir = Path(f'{DATA_DIR}{author_id}/files/')
    zip_list = list(tx_dir.glob('*.zip'))
    return zip_list


def make_workdir(author_id):
    out_dir = Path(f'{OUTPUT_DIR}{author_id}/')  # ファイル出力先
    tx_org_dir = Path(out_dir / './org/')  # 元テキストのUTF-8変換ファイルの保存先
    tx_edit_dir = Path(out_dir / './edit/')  # テキスト整形後のファイル保存先
    return tx_org_dir, tx_edit_dir


def save_cleanse_text(target_file, author_name, tx_org_dir, tx_edit_dir):
    try:
        print(target_file)
        df_tmp = pd.read_csv(target_file, encoding='cp932', names=['text'])
        if SAVE_UTF8_ORG:
            out_org_file_nm = Path(target_file.stem + '_org_utf-8.tsv')
            df_tmp.to_csv(Path(tx_org_dir / out_org_file_nm), sep='\t',
                          encoding='utf-8', index=None)
        df_tmp_e = text_cleanse_df(df_tmp, author_name)
        if WRITE_TITLE:
            df_tmp_e['title'] = df_tmp['text'][0]  # タイトル列を作る
        out_edit_file_nm = Path(target_file.stem + '_clns_utf-8.txt')
        df_tmp_e.to_csv(Path(tx_edit_dir / out_edit_file_nm), sep='\t',
                        encoding='utf-8', index=None, header=WRITE_HEADER)
    except:
        print(f'ERROR: {target_file}')


@click.command()
@click.option('--author_id', '-i', type=str, default='000879')
def main(author_id):
    # author_name = select_author_name(author_id)
    author_name = "芥川 竜之介"
    zip_list = make_ziplist(author_id)
    tx_org_dir, tx_edit_dir = make_workdir(author_id)
    tx_edit_dir.mkdir(exist_ok=True, parents=True)
    print(zip_list)
    if SAVE_UTF8_ORG:
        tx_org_dir.mkdir(exist_ok=True, parents=True)
    for target_file in zip_list:
        save_cleanse_text(target_file, author_name, tx_org_dir, tx_edit_dir)


if __name__ == '__main__':
    main()
