# -*- coding: utf-8 -*-
"""
One-line description of this module. E.g.

This is a more extensive description (optional) that describes the readers implemented
in this module and other relevant information.
"""

# Import the needed libraries
import numpy as np
import gzip
import pyproj

from datetime import datetime, timedelta
from urllib import request
import os
import xmltodict

### Uncomment the next lines if pyproj is needed for the importer.
# try:
#     import pyproj
#
#     PYPROJ_IMPORTED = True
# except ImportError:
#     PYPROJ_IMPORTED = False

from pysteps.decorators import postprocess_import


# Function importer_cwb_compref_cwb to import cwb-format
# files from the ABC institution

# IMPORTANT: The name of the importer should follow the "importer_institution_format"
# naming convention, where "institution" is the acronym or short-name of the
# institution. The "importer_" prefix to the importer name is MANDATORY since it is
# used by the pysteps interface.
#
# Check the pysteps documentation for examples of importers names that follow this
# convention:
# https://pysteps.readthedocs.io/en/latest/pysteps_reference/io.html#available-importers
#
# The function prototype for the importer's declaration should have the following form:
#
#  @postprocess_import()
#  def import_institution_format(filename, keyword1="some_keyword", keyword2=10, **kwargs):
#
# The @postprocess_import operator
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The `pysteps.io.importers` module uses the `postprocess_import` decorator to easily
# define the default data type and default value used for the missing/invalid data.
# The allowed postprocessing operations are
#   - Data type casting using the `dtype` keyword.
#   - Set invalid or missing data to a predefined value using the `fillna` keyword.
# The @postprocess_import decorator should always be added immediately above the
# importer definition to maintain full compatibility with the pysteps library.
# Adding the decorator @add_postprocess_keywords() without any keywords will ensure that
# the precipitation data returned by the importer has double precision, and the
# invalid/missing data is set to `np.nan`.
# For more information on the postprocessing decorator, see:
# https://pysteps.readthedocs.io/en/latest/generated/pysteps.decorators.postprocess_import.html
#
# Function arguments
# ~~~~~~~~~~~~~~~~~~
#
# The function arguments should have the following form:
# (filename, keyword1="some_keyword", keyword2=10,...,keywordN="something", **kwargs)
# The `filename` and `**kwargs` arguments are mandatory to comply with the pysteps
# interface. To fine-control the behavior of the importer, additional keywords can be
# added to the function.
# For example: keyword1="some_keyword", keyword2=10, ..., keywordN="something"
# It is recommended to declare the keywords explicitly in the function to improve the
# readability.
#
#
# Return arguments
# ~~~~~~~~~~~~~~~~
#
# The importer should always return the following fields:
#
# precipitation : 2D array (ndarray or MaskedArray)
#     Precipitation field in mm/h. The dimensions are [latitude, longitude].
# quality : 2D array or None
#     If no quality information is available, set to None.
# metadata : dict
#     Associated metadata (pixel sizes, map projections, etc.).
#
#

@postprocess_import()
def importer_cwb_compref_cwb(filename, gzipped=False, **kwargs):
    """
    A detailed description of the importer. A minimal documentation is
    strictly needed since the pysteps importers interface expect docstrings.

    For example, a documentation may look like this:

    Import a precipitation field from the Awesome Bureau of Composites stored in
    Grib format.

    Parameters
    ----------
    filename : str
        Name of the file to import.

    keyword1 : str
        Some keyword used to fine control the importer behavior.

    keyword2 : int
        Another keyword used to fine control the importer behavior.

    {extra_kwargs_doc}

    ####################################################################################
    # The {extra_kwargs_doc} above is needed to add default keywords added to this     #
    # importer by the pysteps.decorator.postprocess_import decorator.                  #
    # IMPORTANT: Remove these box in the final version of this function                #
    ####################################################################################

    Returns
    -------
    precipitation : 2D array, float32
        Precipitation field in mm/h. The dimensions are [latitude, longitude].
    quality : 2D array or None
        If no quality information is available, set to None.
    metadata : dict
        Associated metadata (pixel sizes, map projections, etc.).
    """

    ### Uncomment the next lines if pyproj is needed for the importer
    # if not PYPROJ_IMPORTED:
    #     raise MissingOptionalDependency(
    #         "pyproj package is required by importer_cwb_compref_cwb
    #         "but it is not installed"
    #     )

    ####################################################################################
    # Add the code to read the precipitation data here. Note that only cartesian grid
    # are supported by pysteps!

    # In this example, we are going create a precipitation fields of only zeros.
    #precip = np.zeros((100, 100), dtype="double")
    # The "double" precision is used in this example to indicate that the imaginary
    # grib file stores the data using double precision.

    # Quality field, should have the same dimensions of the precipitation field.
    # Use None is not information is available.
    quality = None

    # Adjust the metadata fields according to the file format specifications.
    # For additional information on the metadata fields, see:
    # https://pysteps.readthedocs.io/en/latest/pysteps_reference/io.html#pysteps-io-importers

    # The projection definition is an string with a PROJ.4-compatible projection
    # definition of the cartographic projection used for the data
    # More info at: https://proj.org/usage/projections.html

    # For example:

    if gzipped is False:
        fid = open(filename, mode='rb')
    else:
        gz_fid = gzip.open(filename, 'rb')
        fid = gz_fid.read()

    yyyy,mm,dd,hh,mn,ss,nx,ny,nz = np.frombuffer(fid, dtype=np.int32, count=9)
    proj = np.frombuffer(fid, dtype='S4', count=1, offset=36)
    map_scale,projlat1,projlat2,projlon = np.frombuffer(fid, dtype=np.int32, count=4, offset=40)
    alon,alat,xy_scale,dx,dy,dxy_scale = np.frombuffer(fid, dtype=np.int32, count=6, offset=56)
    zht = np.frombuffer(fid, dtype=np.int32, count=nz, offset=80)
    z_scale,i_bb_mode = np.frombuffer(fid, dtype=np.int32, count=2, offset=80+4*nz)
    unkn01 = np.frombuffer(fid, dtype=np.int32, count=9, offset=88+4*nz)
    varname1 = np.frombuffer(fid, dtype='S4', count=1, offset=124+4*nz)
    varname2 = np.frombuffer(fid, dtype=np.int32, count=4, offset=128+4*nz)
    varunit,unkn02 = np.frombuffer(fid, dtype='S3', count=2, offset=144+4*nz)
    var_scale,missing,nradar = np.frombuffer(fid, dtype=np.int32, count=3, offset=150+4*nz)
    mosradar = np.frombuffer(fid, dtype=np.int32, count=nradar, offset=162+4*nz)
    var = np.frombuffer(fid, dtype=np.int16, count=-1, offset=162+4*nz+4*nradar)
    gz_fid.close()

    dBZ = var/var_scale
    dBZ[dBZ<-990] = np.nan # -999 = No Value, -99 = Clear Sky
    precip = dBZ.reshape(ny,nx)

    ul_lon = alon/xy_scale # 115.0
    ul_lat = alat/xy_scale-(ny-1)*(dy/dxy_scale) # 18.0
    lr_lon = alon/xy_scale+(nx-1)*(dx/dxy_scale) # 126.5
    lr_lat = alat/xy_scale # 29.0

    lons = np.linspace(ul_lon, lr_lon, nx)
    lats = np.linspace(ul_lat, lr_lat, ny)

    lons, lats = np.meshgrid(lons, lats)

    pr = pyproj.Proj('EPSG:3826') # TWD97

    x1, y1 = pr(ul_lon, ul_lat)
    x2, y2 = pr(lr_lon, lr_lat)

    metadata = dict(
        xpixelsize=nx,
        ypixelsize=ny,
        cartesian_unit="m",
        unit="dBZ",
        transform="dB",
        zerovalue=-99.0,
        institution="Central Weather Bureau",
        projection="EPSG:3826", 
        yorigin="lower",
        threshold=0,
        x1=x1,
        x2=x2,
        y1=y1,
        y2=y2,
        zr_a=23.5,
        zr_b=1.65,
    )

    # IMPORTANT! The importers should always return the following fields:
    return precip, quality, metadata


def download_cwb_opendata(
        path="./radar/cwb_opendata",
        remove_exist=True,
        authorization="CWB-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        limit=10,
        offset=0,
        timeFrom=(datetime.now()-timedelta(seconds=3600*2)).strftime("%Y-%m-%d %H:%M:%S"),
        timeTo=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), **kwargs):
    """
    A detailed description of the importer. A minimal documentation is
    strictly needed since the pysteps importers interface expect docstrings.

    For example, a documentation may look like this:

    Import a precipitation field from the Awesome Bureau of Composites stored in
    Grib format.

    Parameters
    ----------
    path : str
        path of the file to save.

    remove_old : bool
        True, False. Remove exist data (default = True)

    authorization : str
        * required 氣象開放資料平台會員授權碼

    limit : int
        限制最多回傳的資料, 預設為10

    offset : int
        指定從第幾筆後開始回傳, 預設為第 0 筆開始回傳

    timeFrom : str
        時間區段, 篩選需要之時間區段，時間從「timeFrom」開始篩選，直到內容之最後時間，並可與參數「timeTo」 合併使用，格式為「yyyy-MM-dd hh:mm:ss」

    timeTo : str
        時間區段, 篩選需要之時間區段，時間從內容之最初時間開始篩選，直到「timeTo」，並可與參數「timeFrom」 合併使用，格式為「yyyy-MM-ddThh:mm:ss」

    {extra_kwargs_doc}

    ####################################################################################
    # The {extra_kwargs_doc} above is needed to add default keywords added to this     #
    # importer by the pysteps.decorator.postprocess_import decorator.                  #
    # IMPORTANT: Remove these box in the final version of this function                #
    ####################################################################################

    Returns
    -------

    None

    """
    
    if remove_exist:
        import shutil
        os.makedirs(path, exist_ok=True)
        shutil.rmtree(path)        

    timeFrom2 = datetime.strptime(timeFrom, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%dT%H%%3A%M%%3A%S")
    timeTo2 = datetime.strptime(timeTo, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%dT%H%%3A%M%%3A%S")
    urlc = 'https://opendata.cwb.gov.tw/historyapi/v1/getMetadata/O-A0059-001' + '?Authorization=' + authorization + '&limit=' + str(limit) + '&offset=' + str(offset) + '&format=' + 'XML' + '&timeFrom=' + timeFrom2 + '&timeTo='  +timeTo2
    
    RawDataList = xmltodict.parse(request.urlopen(urlc).read().decode("utf-8"))
    
    TList = RawDataList['cwbopendata']['dataset']['resources']['resource']['data']['time']
    
    for i in np.arange(0,np.size(TList,0),1):
        tLnum  = datetime.strptime(TList[i]['dataTime'], '%Y-%m-%d %H:%M:%S').timestamp()
        tLyy = datetime.utcfromtimestamp(tLnum).strftime('%Y')
        tLmm = datetime.utcfromtimestamp(tLnum).strftime('%m')
        tLdd = datetime.utcfromtimestamp(tLnum).strftime('%d')
        tLhh = datetime.utcfromtimestamp(tLnum).strftime('%H')
        tLmn = datetime.utcfromtimestamp(tLnum).strftime('%M')
        tLpath = path+'/'+tLyy+'/'+tLmm+'/'+tLdd+'/COMPREF.OpenData.'+tLyy+tLmm+tLdd+'.'+tLhh+tLmn+'.gz'
        
        os.makedirs(path, exist_ok=True)
        if not os.path.isfile(tLpath):
            print("Making file:  "+tLpath)
            url = TList[i]['url']

            RawData = xmltodict.parse(request.urlopen(url).read().decode("utf-8"))

            parameterSet = RawData['cwbopendata']['dataset']['datasetInfo']['parameterSet']['parameter']

            lon0 =  np.fromstring(parameterSet[1]['parameterValue'],
                                  dtype=np.float16,
                                  count=-1,
                                  sep=',')[0]

            lat0 =  np.fromstring(parameterSet[1]['parameterValue'],
                                  dtype=np.float16,
                                  count=-1,
                                  sep=',')[1]

            res = float(parameterSet[2]['parameterValue'])

            t0 = parameterSet[3]['parameterValue']
            t0num   = datetime.strptime(t0, '%Y-%m-%dT%H:%M:%S%z').timestamp()
            utct0 = datetime.utcfromtimestamp(t0num).strftime('%Y-%m-%d %H:%M:%S')

            nx = np.fromstring(parameterSet[4]['parameterValue'],
                              dtype=np.int16,
                              count=-1,
                              sep='*')[0]

            ny = np.fromstring(parameterSet[4]['parameterValue'],
                              dtype=np.int16,
                              count=-1,
                              sep='*')[1]

            unit = parameterSet[5]['parameterValue']

            dbz = np.fromstring(RawData['cwbopendata']['dataset']['contents']['content'],
                                dtype=np.float32,
                                count=-1,
                                sep=',').astype(np.int16)

            dbz = dbz.reshape(ny,nx)

            # import matplotlib.pyplot as plt
            # lon,lat = np.meshgrid(
            #     np.arange(lon0,lon0+res*(x-1)+res/2,res),
            #     np.arange(lat0,lat0+res*(y-1)+res/2,res))
            # plt.pcolor(lon,lat,dbz)

            yyyy = utct0[0:4]
            mm = utct0[5:7]
            dd = utct0[8:10]
            hh = utct0[11:13]
            mn = utct0[14:16]
            ss = utct0[17:19]
            nz = 1
            # allocate(var4(nx,ny,nz),var_true(nx,ny,nz),var(nx,ny,nz))
            # allocate(I_var_true(nx,ny,nz))
            # allocate(zht(nz))
            proj = 'LL'
            map_scale = 1000
            projlat1 = 30*map_scale
            projlat2 = 60*map_scale
            projlon = 120.75*map_scale
            xy_scale = 1000
            alon = lon0*xy_scale
            alat = (lat0+res*(ny-1))*xy_scale
            dxy_scale = 100000
            dx = res*dxy_scale
            dy = res*dxy_scale
            zht = 0
            z_scale = 1
            i_bb_mode = -12922
            unkn01 = np.zeros(9)
            varname1 = ['Q','P','E','O']
            varname2 = [1,2,3,4]
            varunit = unit
            unkn02 = 'TRA'
            var_scale = 10
            missing = -999
            nradar = 1
            mosradar = 'AAAA'

            os.makedirs(path+'/'+tLyy+'/'+tLmm+'/'+tLdd, exist_ok=True)
         
            #write BUFFER
            
            buffer = np.array([yyyy,mm,dd,hh,mn,ss,nx,ny,nz], dtype='i4').tobytes()
            buffer += np.array(proj, dtype='a4').tobytes()
            buffer += np.array([map_scale,projlat1,projlat2,projlon,alon,alat,xy_scale,dx,dy,
                      dxy_scale,zht,z_scale,i_bb_mode], dtype='i4').tobytes()
            buffer += np.array(unkn01, dtype='i4').tobytes()
            buffer += np.array(varname1, dtype='a1').tobytes()
            buffer += np.array(varname2, dtype='i4').tobytes()
            buffer += np.array(varunit, dtype='a3').tobytes()
            buffer += np.array(unkn02, dtype='a3').tobytes()
            buffer += np.array([var_scale,missing,nradar], dtype='i4').tobytes()
            buffer += np.array(mosradar, dtype='a4').tobytes()

            dbz1d = dbz.flatten()
            buffer += np.array(dbz1d*var_scale, dtype='i2').tobytes()
            gz_fid = gzip.open(tLpath, 'wb')
            gz_fid.write(buffer)
            gz_fid.close()
    return None