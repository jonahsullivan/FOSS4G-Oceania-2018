from osgeo import gdal, ogr
import os
import sys

# set the input data
# dem_filename = r"C:\temp\DEM.tif"
dem_filename = sys.argv[1]
# shp_filename = r"C:\temp\testLines.shp"
shp_filename = sys.argv[2]

# open the elevation data
src_ds = gdal.Open(dem_filename)
geotransform = src_ds.GetGeoTransform()
raster_band = src_ds.GetRasterBand(1)

# open the line data
in_ds = ogr.Open(shp_filename)
in_lyr = in_ds.GetLayer()
in_lyr_dfn = in_lyr.GetLayerDefn()
in_srs = in_lyr.GetSpatialRef()

# open the output data
out_shp_filename = shp_filename.split(os.extsep)[0] + "_slope.shp"
out_driver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(out_shp_filename):
    out_driver.DeleteDataSource(out_shp_filename)
out_ds = out_driver.CreateDataSource(out_shp_filename)
out_srs = in_srs
out_lyr = out_ds.CreateLayer(os.path.basename(out_shp_filename.split(os.extsep)[0]),
                             srs=in_srs,
                             geom_type=ogr.wkbLineString)

# create empty fields in output data
for i in range(0, in_lyr_dfn.GetFieldCount()):
    field_definition = in_lyr_dfn.GetFieldDefn(i)
    out_lyr.CreateField(field_definition)

# create an additional field for slope
slope_field = ogr.FieldDefn("slope", ogr.OFTReal)
out_lyr.CreateField(slope_field)
out_lyr_dfn = out_lyr.GetLayerDefn()

# loop through the lines writing to new shapefile
for in_feat in in_lyr:
    geom = in_feat.GetGeometryRef()
    start_elev = 0
    end_elev = 0
    for point_num in range(geom.GetPointCount()):
        point = geom.GetPoint(point_num)

        mx, my = point[0], point[1]  # coord in map units

        # Convert from map to pixel coordinates.
        # Only works for geotransforms with no rotation.
        px = int((mx - geotransform[0]) / geotransform[1])  # x pixel
        py = int((my - geotransform[3]) / geotransform[5])  # y pixel

        intval = raster_band.ReadAsArray(px, py, 1, 1)

        if point_num == 0:
            start_elev = intval[0][0]

        if point_num == geom.GetPointCount():
            end_elev = intval[0][0]

    # Add field values from input layer
    out_feat = ogr.Feature(out_lyr_dfn)
    for i in range(0, in_lyr_dfn.GetFieldCount()):
        out_feat.SetField(out_lyr_dfn.GetFieldDefn(i).GetNameRef(), in_feat.GetField(i))
        
    # copy over the geometry
    out_feat.SetGeometry(geom)

    # add slope value
    slope = (start_elev - end_elev) / geom.Length()
    out_feat.SetField("slope", float(slope))

    # create the output feature
    out_lyr.CreateFeature(out_feat)

    # cleanup
    feature = None
