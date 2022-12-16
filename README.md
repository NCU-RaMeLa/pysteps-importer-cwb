<h1 align="center">pySTEPS Importer (CWB composite Radar data)</h1>

### 此module為[pySTEPS](https://github.com/pySTEPS/pysteps)之延伸模組，無法單一使用


# 相關網站
* [pySTEPS](https://pysteps.readthedocs.io)
* [pySTEPS-GitHub](https://github.com/pySTEPS/pysteps)
* [NCU RADAR Lab.](http://radar.atm.ncu.edu.tw)
* [CWB Open Weather Data](https://opendata.cwb.gov.tw)
* [Central Weather Bureau](https://www.cwb.gov.tw)


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
from pysteps_importer_cwb.importer_cwb_compref import importer_cwb_compref_xxx
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
importer = importer_cwb_compref_xxx
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
importer = importer_cwb_compref_xxx
R, quality, metadata = pysteps.io.read_timeseries(fns, importer, **importer_kwargs)

###############################################################################
```
