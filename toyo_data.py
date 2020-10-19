from pathlib import Path
from datetime import datetime 
import pandas as pd
import requests 
import xml.etree.ElementTree as ET

def make_date_path(date_now: datetime, base_path: Path) -> Path: 
    p = Path(f"./{date_now.year}/{date_now.month:02}/{date_now.year}_{date_now.month:02}_{date_now.day:02}.csv")
    base_plus_p = base_path.joinpath(p)
    return base_plus_p

def now_datetime_str(date_now: datetime) -> Path:
    now_str = f"{date_now.year}{date_now.month:02}{date_now.day:02}{date_now.hour:02}{date_now.minute:02}"
    return now_str

def str_to_datetime(str_date: str) -> datetime:
    if len(str_date) == 12:
        year = int(str_date[:4])
        month = int(str_date[4:6])
        day = int(str_date[6:8])
        hour = int(str_date[8:10])
        minutes = int(str_date[10:])
        return datetime(year, month, day, hour, minutes)
    pass

def mkdir_with_pathlib(path: Path) -> None:
    """
    pathはディレクトリ名で渡す
    """
    
    if not path.exists():
        try:
            path.mkdir()
        except:
            mkdir_with_pathlib(path.parent)
            mkdir_with_pathlib(path)

def make_dict_for_dataframe(data: list, col_names: list) -> dict:
    """
    コラム名とデータから辞書を作成する
    これを使ってデータフレームを作成する
    """
    data_dict = dict()
    for col_name, d in zip(col_names, data):
        data_dict[col_name] = [d]
    return data_dict
    
            
def open_new_csv(path: Path, data_dict: dict, now_str: str) -> None:
    """
    csvファイルがなければファイルを作成し、
    その日の分のファイルに、
    新たなデータフレームを保存する
    """
    test = path.open("w")
    test.close()
    df = pd.DataFrame(data_dict)
    df.index = [now_str]
    df.to_csv(path)
    
if __name__ == "__main__":

    r = requests.get(xml_url)
    if r.status_code == 200:
        # XMLの読み込み
        tree = ET.fromstring(r.content)
        dt = tree[0].attrib["date"]
        # datetimeのパスの作成
        dt_dt = str_to_datetime(dt)
        dt_path = make_date_path(dt_dt)
        now_str = now_datetime_str(dt_dt)
        # データの作成
        factors = []
        for i in range(len(tree[0])):
            factors.append(tree[0][i].attrib["value"])
        if dt_path.exists():
            df = pd.read_csv(dt_path, index_col=0)
            df.loc[dt] = factors 
            df.to_csv(dt_path)
        else:
            mkdir_with_pathlib(dt_path.parent)
            data_dict = make_dict_for_dataframe(factors, toyohashi_cols_name)
            open_new_csv(dt_path, data_dict, now_str)