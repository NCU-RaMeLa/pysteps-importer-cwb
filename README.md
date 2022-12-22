<h1 align="center">pySTEPS Importer (CWB composite Radar data)</h1>

### 此module為[pySTEPS](https://github.com/pySTEPS/pysteps)之延伸模組，無法單一使用


# 相關網站
* [pySTEPS](https://pysteps.readthedocs.io)
* [pySTEPS-GitHub](https://github.com/pySTEPS/pysteps)
* [NCU RADAR Lab.](http://radar.atm.ncu.edu.tw)
* [CWB Open Weather Data](https://opendata.cwb.gov.tw)
* [Central Weather Bureau](https://www.cwb.gov.tw)

# 額外會用到的module:
os<br>
urllib3<br>
datetime<br>

# 支援的檔案格式
支援氣象局二維全台雷達整合資料之gzip壓縮格式 (e.q. COMPREF.20211127.1430.gz)<br>
P.S.若已解壓縮，則gzipped自行改成false


# 如何應用於pySTEPS
### 1. 將pysteps-importer-cwb放置於和python檔同目錄下
pysteps-importer-cwb/內應該會有docs, pysteps_importer_cwb, tests, ......等資料


### 2. 如何import
建議先import pystep後再import此moudle
```python
import pysteps
import sys
sys.path.append('./pysteps-importer-cwb')
from pysteps_importer_cwb.importer_cwb_compref import importer_cwb_compref_cwb
```

### 3. 使用此module
通常在import雷達資料時，依照pySTEPS建議說明為:
```python
date = datetime.strptime("201009190600", "%Y%m%d%H%M")
fns = pysteps.io.archive.find_by_date(date, root_path, path_fmt, fn_pattern, fn_ext, timestep=10, num_prev_files=9)
importer = pysteps.io.get_method(importer_name, "importer")
R, quality, metadata = pysteps.io.read_timeseries(fns, importer, **importer_kwargs)
```

使用此module後，改成使用以下方式進行import即可:
```python
date = datetime.strptime("201009190600", "%Y%m%d%H%M")
importer = importer_cwb_compref_cwb
fns = pysteps.io.archive.find_by_date(date, root_path="./radar/cwb", path_fmt="%Y/%m/%d", fn_pattern="COMPREF.%Y%m%d.%H%M", fn_ext="gz", timestep=10, num_prev_files=9)
R, quality, metadata = pysteps.io.read_timeseries(fns, importer, **importer_kwargs)
```

### 使用pystepsrc.json之情況
pySTEPS有提供[pystepsrc.json](https://pysteps.readthedocs.io/en/stable/user_guide/pystepsrc_example.html)之範例，若使用客製化pystepsrc.json檔，則須在檔案中加入:
```json
        "cwb": {
            "root_path": "./radar/cwb",
            "path_fmt": "%Y/%m/%d",
            "fn_pattern": "COMPREF.%Y%m%d.%H%M",
            "fn_ext": "gz",
            "importer": "cwb_compref",
            "timestep": 10,
            "importer_kwargs": {
                "gzipped": true
            }
        }
```

加入後即可以下列方式讀取
```python
################################################################################
# Read the radar input images
# ---------------------------
#
# First, we will import the sequence of radar composites.
# You need the pysteps-data archive downloaded and the pystepsrc file
# configured with the data_source paths pointing to data folders.

# Selected case
date = datetime.strptime("201701311030", "%Y%m%d%H%M")
date = datetime.strptime("201009190600", "%Y%m%d%H%M")


# Import pysteps and load the new configuration file
config_file_path = './pystepsrc.json'
_ = pysteps.load_config_file(config_file_path, verbose=True)
# The default parameters are stored in pysteps.rcparams.
data_source = pysteps.rcparams.data_sources["cwb"]

###############################################################################
# Load the data from the archive
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root_path = data_source["root_path"]
path_fmt = data_source["path_fmt"]
fn_pattern = data_source["fn_pattern"]
fn_ext = data_source["fn_ext"]
importer_name = data_source["importer"]
importer_kwargs = data_source["importer_kwargs"]
timestep = data_source["timestep"]

# Find the input files from the archive
fns = pysteps.io.archive.find_by_date(
    date, root_path, path_fmt, fn_pattern, fn_ext,
    timestep=10, num_prev_files=9)

# Read the radar composites
#importer = pysteps.io.get_method(importer_name, "importer")
importer = importer_cwb_compref_cwb
R, quality, metadata = pysteps.io.read_timeseries(fns, importer, **importer_kwargs)

###############################################################################
```

# 下載 CWB Open weather data
此module另有CWB open data雷達回波資料下載用插件方便即時import雷達資料<br>
(需要有氣象會員授權碼: CWB-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)<br>
預設存檔於 './radar/cwb_opendata', 檔名為COMPREF.OpenData.yyyymmdd.HHMM.gz<br>
向CWB請求資料下載時與查找資料之時間區間為使用台灣時間(UTC+8)<br>
下載後之檔名與檔頭內容皆會轉為UTC<br>

### 快速使用方式:
```python
from pysteps_importer_cwb.importer_cwb_compref import download_cwb_opendata

download_data = download_cwb_opendata(authorization="CWB-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX")
# CWB-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX 請自行替換成您的API授權碼

'''
Parameters
    ----------
    path : str (defualt = './radar/cwb_opendata')
        檔案儲存路徑 (配合pySTEPS範例資料路徑)

    remove_old : bool (default = True)
        True 或 False. True則會刪除給定的path資料夾

    authorization : str
        * required 氣象開放資料平台會員授權碼

    limit : int (default = 10)
        限制最多回傳的資料, 預設為10

    offset : int (defaule = 0)
        指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳

    timeFrom : str (UTC+8)
        時間區段, 篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數「timeTo」 合併使用，格式為「yyyy-MM-dd hh:mm:ss」

    timeTo : str (UTC+8)
        時間區段, 篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」
'''
```

若為快速使用方式, 預設存儲路徑為 ./radar/cwb_opendata<br>
會先刪除 ./radar/cwb_opendata 資料夾後再重新建立資料夾進行下載<br>
並從 https://opendata.cwb.gov.tw 下載最新10筆雷達回波資料<br>

### 進階使用:
```python
from pysteps_importer_cwb.importer_cwb_compref import download_cwb_opendata

download_data = download_cwb_opendata(
    path="./radar/cwb_opendata",
    remove_exist=False, # 不刪除任何資料(!!硬碟使用將會越來越多!!)
    authorization="CWB-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    limit=20, # 回傳20筆清單
    offset=3, # 從第 3 筆開始回傳
    timeFrom="2022-12-06 10:22:32", # 從 2022/12/06 10:22:32 (UTC+8) 開始
    timeTo="2022-12-20 05:12:49" # 到 2022/12/20 05:12:49 (UTC+8) 結束, 此時間段CWB擁有的資料
    )
```

接著修改 importer 所需要的資訊, 將
```python
root_path="./radar/cwb"
fn_pattern="COMPREF.%Y%m%d.%H%M"
```
改成
```python
root_path="./radar/cwb_opendata"
fn_pattern="COMPREF.OpenData.%Y%m%d.%H%M"
```
即可應用於pySTEPS中
