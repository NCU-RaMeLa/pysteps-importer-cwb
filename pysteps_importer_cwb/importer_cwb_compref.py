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
