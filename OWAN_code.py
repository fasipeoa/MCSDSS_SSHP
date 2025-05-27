# Elevation 

# MOSAIC TO NEW RASTER

with arcpy.EnvManager(resamplingMethod="CUBIC", pyramid="PYRAMIDS -1 CUBIC DEFAULT 75 NO_SKIP NO_SIPS"):
    arcpy.management.MosaicToNewRaster(
        input_rasters="n07_e005_1arc_v3.tif;n06_e006_1arc_v3.tif;n07_e006_1arc_v3.tif;n06_e005_1arc_v3.tif",
        output_location=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb",
        raster_dataset_name_with_extension="OWAN_MERGED",
        coordinate_system_for_the_raster='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
        pixel_type="16_BIT_UNSIGNED",
        cellsize=None,
        number_of_bands=1,
        mosaic_method="LAST",
        mosaic_colormap_mode="FIRST"
    )


FILL DEM

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_surface_raster = arcpy.sa.Fill(
        in_surface_raster="OWAN_MERGED",
        z_limit=None
    )
    out_surface_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\OWAN_FILL_DEM")


# PROJECT RASTER

arcpy.management.ProjectRaster(
    in_raster="OWAN_FILL_DEM",
    out_raster=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\OWAN_FILL_DEM_ProjectRaster",
    out_coor_system='PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    resampling_type="CUBIC",
    cell_size="30 30",
    geographic_transform=None,
    Registration_Point=None,
    in_coor_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
    vertical="NO_VERTICAL"
)

# EXTRACT BY MASK DEM = Owan_Elevation

with arcpy.EnvManager(outputCoordinateSystem='PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster="OWAN_FILL_DEM_ProjectRaster",
        in_mask_data="Owan Watershed Boundary",
        extraction_area="INSIDE",
        analysis_extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation")

# CLASSIFY ELEVATION

# Reclass Elevation

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Elevation",
        reclass_field="Value",
        remap="49 250 1;250 402 2",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Elevation")


# USE ELEVATION MAP TO SET ENVIRONMENT



# SLOPE MAP

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Slope(
        in_raster="Owan_Elevation",
        output_measurement="DEGREE",
        z_factor=1,
        method="PLANAR",
        z_unit="METER",
        analysis_target_device="GPU_THEN_CPU"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Slope")


# CLASSIFY SLOPE

# Reclass Slope

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Slope",
        reclass_field="VALUE",
        remap="0 2 1;2 8 5;8 16 4;16 30 3;30 40.491734 2",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Slope")


# FLOW DIRECTION

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_flow_direction_raster = arcpy.sa.FlowDirection(
        in_surface_raster="Owan_Elevation",
        force_flow="NORMAL",
        out_drop_raster=None,
        flow_direction_type="D8"
    )
    out_flow_direction_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Flow_Direction")


# FLOW ACCUMULATION

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_accumulation_raster = arcpy.sa.FlowAccumulation(
        in_flow_direction_raster="Owan_Flow_Direction",
        in_weight_raster=None,
        data_type="FLOAT",
        flow_direction_type="D8"
    )
    out_accumulation_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Flow_Accumulation")


# STREAM ORDER
# Raster Calculator

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' "Owan_Flow_Accumulation" >1200'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Raster_Calc")

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.StreamOrder(
        in_stream_raster="Owan_Raster_Calc",
        in_flow_direction_raster="Owan_Flow_Direction",
        order_method="STRAHLER"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_Order")

# STREAM TO FEATURE (Stream_Order)

arcpy.sa.StreamToFeature(
    in_stream_raster="Owan_Stream_Order",
    in_flow_direction_raster="Owan_Flow_Direction",
    out_polyline_features=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_to_Feature",
    simplify="SIMPLIFY"
)

# Stream to Feature (Stream Order) Polyline to Raster

arcpy.conversion.PolylineToRaster(
    in_features="Owan_Stream_to_Feature",
    value_field="grid_code",
    out_rasterdataset=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_Order_Raster",
    cell_assignment="MAXIMUM_LENGTH",
    priority_field="NONE",
    cellsize=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
    build_rat="BUILD"
)

# Reclassify Stream to feature (Stream Order) 

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Stream_Order_Raster",
        reclass_field="Value",
        remap="1 1;2 2;3 3;4 4",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order")



# STREAM POWER INDEX

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' Ln("Owan_Flow_Accumulation" *"Owan_Slope" )'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_Power_Index")

# Reclassify Stream Power Index

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Stream_Power_Index",
        reclass_field="VALUE",
        remap="-1.726308 0.300000 1;0.300000 0.500000 2;0.500000 1.010000 3;1.010000 5.100000 4;5.100000 14.706011 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Power_Index")



# Drainage Density

# Raster to Polyline

arcpy.conversion.RasterToPolyline(
    in_raster="Owan_Raster_Calc",
    out_polyline_features=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Raster_to_Polyline",
    background_value="ZERO",
    minimum_dangle_length=0,
    simplify="SIMPLIFY",
    raster_field="Value"
)

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.LineDensity(
        in_polyline_features="Owan_Raster_to_Polyline",
        population_field="NONE",
        cell_size=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
        search_radius=1396.9813349878339,
        area_unit_scale_factor="SQUARE_KILOMETERS"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Drainage_Density")

# CLASSIFY DRAINAGE DENSITY

# Reclassify Drainage Density

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Drainage_Density",
        reclass_field="VALUE",
        remap="0 0.550000 1;0.550000 2.670000 2;2.670000 3.440000 3;3.440000 4.750000 4;4.750000 100 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density")


# TOPOGRAPHIC WETNESS INDEX

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression='( "Owan_Flow_Accumulation"+1) *30'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\A")

# Slope in Radian

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' "Owan_Slope" *0.01745329'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Slope_Radian")

# Slope Radian Tan

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' Con("Owan_Slope_Radian" >0, Tan("Owan_Slope_Radian"),0.001 )'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Slope_Radian_Tan")

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' Ln("A" /"Owan_Slope_Radian_Tan" )'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_TWI")

# Reclassify TWI

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_TWI",
        reclass_field="VALUE",
        remap="3.831447 4 1;4 8 2;8 13 3;13 17 4;17 23.221071 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI")


# DISCHARGE

# Project HydroRIVER Data

arcpy.management.Project(
    in_dataset="HydroRIVERS_v10_af",
    out_dataset=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\HydroRIVERS_v10_af_Project",
    out_coor_system='PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    transform_method=None,
    in_coor_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
    preserve_shape="NO_PRESERVE_SHAPE",
    max_deviation=None,
    vertical="NO_VERTICAL"
)

# Clip Discharge River Network

arcpy.analysis.Clip(
    in_features="HydroRIVERS_v10_af_Project",
    clip_features="Owan Watershed Boundary",
    out_feature_class=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_Discharge",
    cluster_tolerance=None
)

# Stream Discharge Polyline to Raster

arcpy.conversion.PolylineToRaster(
    in_features="Owan_Stream_Discharge",
    value_field="DIS_AV_CMS",
    out_rasterdataset=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Stream_Discharge_Raster",
    cell_assignment="MAXIMUM_LENGTH",
    priority_field="NONE",
    cellsize=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
    build_rat="BUILD"
)

# Reclassify Stream Discharge

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Stream_Discharge_Raster",
        reclass_field="VALUE",
        remap="0.112000 1;0.112000 0.500000 2;0.500000 1 3;1 2 4;2 144.593994 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Discharge")



# RAINFALL

# Project Rainfall Raster

arcpy.management.ProjectRaster(
    in_raster="PDIR_1y2022.tif",
    out_raster=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\PDIR_1y2022_ProjectRaster1",
    out_coor_system='PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
    resampling_type="CUBIC",
    cell_size="4454.19479691001 4454.19479691001",
    geographic_transform=None,
    Registration_Point=None,
    in_coor_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]',
    vertical="NO_VERTICAL"
)

# Extract by Mask

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster="PDIR_1y2022.tif",
        in_mask_data="Owan Watershed Boundary",
        extraction_area="INSIDE",
        analysis_extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Rainfall_2022")

# Reclassify Rainfall 

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Rainfall_2022",
        reclass_field="Value",
        remap="1145 1836 3",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Rainfall_2022")


# Population Density

# Extract by Mask

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster="ecreee_ecowpop.tif",
        in_mask_data="Owan Watershed Boundary",
        extraction_area="INSIDE",
        analysis_extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Pop_Density_Ecow")

# Reclassify Population Density

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Pop_Density_Ecow",
        reclass_field="VALUE",
        remap="4.057050 10 1;10 30 2;30 8289.089844 3",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density")

# SOIL MAP

# Clip Soil Map

arcpy.analysis.Clip(
    in_features="DSMW",
    clip_features="Owan Watershed Boundary",
    out_feature_class=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Soil",
    cluster_tolerance=None
)

# Soil Polygon To Raster

arcpy.conversion.PolygonToRaster(
    in_features="Owan_Soil",
    value_field="SNUM",
    out_rasterdataset=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Soil_Raster",
    cell_assignment="CELL_CENTER",
    priority_field="NONE",
    cellsize=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
    build_rat="BUILD"
)

# Reclassify Soil 

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Soil_Raster",
        reclass_field="Value",
        remap="1 1;1 2 2",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil")
# GEOLOGY MAP

# Clip Geology Map

arcpy.analysis.Clip(
    in_features="geo7_2ag",
    clip_features="Owan Watershed Boundary",
    out_feature_class=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Geology",
    cluster_tolerance=None
)

# Geology Polygon To Raster 

arcpy.conversion.PolygonToRaster(
    in_features="Owan_Geology",
    value_field="GLG",
    out_rasterdataset=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Geology_Raster",
    cell_assignment="CELL_CENTER",
    priority_field="NONE",
    cellsize=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
    build_rat="BUILD"
)

# Reclassify Geology 

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Geology_Raster",
        reclass_field="Value",
        remap="1 5;1 2 3;2 3 3",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology")


# EXPORT ROAD DATA 

with arcpy.EnvManager(outputCoordinateSystem='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'):
    arcpy.conversion.ExportFeatures(
        in_features=r"C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp",
        out_features=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\hotosm_nga_roads_lines_shp_ExportFeatures.shp",
        where_clause="",
        use_field_alias_as_name="NOT_USE_ALIAS",
        field_mapping=r'name "name" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,name,0,79;name_en "name_en" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,name_en,0,79;highway "highway" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,highway,0,79;surface "surface" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,surface,0,79;smoothness "smoothness" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,smoothness,0,79;width "width" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,width,0,79;lanes "lanes" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,lanes,0,79;oneway "oneway" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,oneway,0,79;bridge "bridge" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,bridge,0,79;layer "layer" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,layer,0,79;source "source" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,source,0,79;osm_id "osm_id" true true false 18 Double 0 18,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,osm_id,-1,-1;osm_type "osm_type" true true false 80 Text 0 0,First,#,C:\Users\f\Desktop\Study Area\ROADS\hotosm_nga_roads_lines_shp\hotosm_nga_roads_lines_shp.shp,osm_type,0,79',
        sort_field=None
    )

# CLIP ROAD TO WATERSHED

arcpy.analysis.Clip(
    in_features="hotosm_nga_roads_lines_shp_ExportFeatures",
    clip_features="Owan Watershed Boundary",
    out_feature_class=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Road",
    cluster_tolerance=None
)

# Distance TO ROAD

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_distance_raster = arcpy.sa.EucDistance(
        in_source_data="Owan_Road",
        maximum_distance=None,
        cell_size=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
        out_direction_raster=None,
        distance_method="PLANAR",
        in_barrier_data=None,
        out_back_direction_raster=None
    )
    out_distance_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Distance_to_Road")

# CLASSIFY DISTANCE TO ROAD

# Reclassify Distance to Road

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Distance_to_Road",
        reclass_field="VALUE",
        remap="0 1000 5;1000 2500 4;2500 5000 3;5000 7500 2;7500 15000 1",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road")


# Distance TO SETTLEMENT

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_distance_raster = arcpy.sa.EucDistance(
        in_source_data="Town",
        maximum_distance=None,
        cell_size=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
        out_direction_raster=None,
        distance_method="PLANAR",
        in_barrier_data=None,
        out_back_direction_raster=None
    )
    out_distance_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Distance_to_Settlement")

# CLASSIFY DISTANCE TO SETTLEMENT

# Reclassify Distance to Settlement 

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_Distance_to_Settlement",
        reclass_field="VALUE",
        remap="0 250 1;250 2500 5;2500 5000 4;5000 10000 3;10000 12500 2",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement")

# PROTECTED ECOLOGICAL ZONE

# Clip Protected Ecological Zone

arcpy.analysis.Clip(
    in_features="WDPA_poly_Jul2024",
    clip_features="Owan Watershed Boundary",
    out_feature_class=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Protected_Ecological_Zone",
    cluster_tolerance=None
)

# Distance to Protected Ecological Zone

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_distance_raster = arcpy.sa.EucDistance(
        in_source_data="Owan_Protected_Ecological_Zone",
        maximum_distance=None,
        cell_size=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_Elevation",
        out_direction_raster=None,
        distance_method="PLANAR",
        in_barrier_data=None,
        out_back_direction_raster=None
    )
    out_distance_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_DIstance_to_Protected_Ecological_Zone")

# CLASSIFY DISTANCE TO Protected Ecological Zone

# Reclassify Distance to Protected Ecological Zone

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_DIstance_to_Protected_Ecological_Zone",
        reclass_field="VALUE",
        remap="0 2000 1;2000 3000 2;3000 4000 3;4000 5000 4;5000 28371.578125 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone")


# CURVE NUMBER

# Global CN Code
Code link: https://figshare.com/articles/dataset/GCN250_global_curve_number_datasets_for_hydrologic_modeling_and_design/7756202?file=15379361

globalCN <- function (){
  #---Libraries-----------------------------------------------------------------------------------------------------
  library (raster)
  
  #---Change working directory
  setwd("your\\working\\directory")
  
  #---Change temp directory for raster package and create it if it does not exist
  tempdirectory<-"temp\\directory"
  dir.create(tempdirectory,showWarnings = F)
  rasterOptions(tmpdir=tempdirectory)
  
  #---download HYSOGs250m and ESA CCI-LC 2015 from cited depository to the working directory
  #---download the CN look up table from the associated depository

  #---Read the downloaded HYSOGs250m and ESA CCI-LC 2015
  HYSOGs250m <- raster("./HYSOGs250m.tif")
  ESA_CCILC_2015_300m <- raster("./ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7.tif")
  
  #---Crop the ESA CCI-LC 2015 to the extent of HYSOGs250m
  ESA_CCILC_2015_300m <- crop(ESA_CCILC_2015_300m, extent(HYSOGs250m))
  
  #---Resample ESA CCI-LC 2015 to the spatial resolution of HYSOGs250m 
  ESA_CCILC_2015_250m <- resample(ESA_CCILC_2015_300m, HYSOGs250m, method = "ngb")
  
  #---Read the CN lookup table
  CNtable <- read.csv("./CN_Table.csv", stringsAsFactors = F, check.names=FALSE)
  
  #---Create GCN raster with the same properties as HYSOG250m
  GCN250 <- raster(HYSOGs250m)

  #---Reclassify the land cover raster to CN values based on HYSOGs250 and lookup table
  #---Iterate through the soil groups 

  for (j in 3:10) {
   
    #---create land cover raster for soil group j
    LC_j <-  ESA_CCILC_2015_250m
    LC_j [HYSOGtile!=as.integer(colnames(CNtable)[j])] <- 0

    #substitute the land cover values of soil group j by the corresponding CN values from the lookup table 
    LC_j <- subs(x= LC_j,y=CNtable,by=1,which=colnames(CNtable)[j])

    GCN250[HYSOGs250m==as.integer(colnames(CNtable)[j])] <- LC_j[HYSOGs250m==as.integer(colnames(CNtable)[j])]
    
  }
  #write GCN250 to the working folder
  writeRaster(GCN250,"./GCN250.tif" ,format = "GTiff", overwrite=TRUE, dataType = "INT1U",options="COMPRESS=LZW")
}

#Extract by Mask

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster="GCN250_ARCII.tif",
        in_mask_data="Owan Watershed Boundary",
        extraction_area="INSIDE",
        analysis_extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_CN")

# CLASSIFY CN

# Reclassify CN

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_CN",
        reclass_field="Value",
        remap="70 80 3;80 87 4;87 91 5",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN")


# Land Use Land Cover (LULC)

# Dynamic World Code
Code link: https://code.earthengine.google.co.in/59a96e93b6e65622eda56694d277522d

// Download the Real Time Global 10m Dynamic World Land Cover Data

//1. Import Country boundaries
var countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');
var roi = countries.filter(ee.Filter.eq('country_na', 'Nigeria'));

//2. Define start date and end date
var startDate = '2024-01-01';
var endDate = '2024-06-30';

//3. Load DYNAMIC WORLD Data
var dw = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
.filterDate(startDate, endDate);
//.filterBounds(roi);

//4. Clip with countries boundaries

//var dwImage = ee.Image(dw.mosaic()); //.clip(roi);
var dwImage = ee.Image(dw.mosaic()).clip(roi);

print('DW ee.Image', dwImage) ;

//5. Display the the classified image using the label band.
var classification = dwImage.select('label');
var dwVisParams = {
min: 0,
max: 8,
 palette: ['#419BDF', '#397D49', '#888053', '#7A87C6', '#E49635', '#DFC35A', '#C4281B', '#A59B8F', '#B39FE1']
};

Map.addLayer(classification, dwVisParams, 'Classified Image');
Map.centerObject(roi);

//6. Export classified map to Google Drive
Export.image.toDrive({
  image: classification,
  description: 'Dynamic_World_2024',
  scale: 10,
  region: roi,
  maxPixels: 1e13,
});

# Extract by Mask

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.ExtractByMask(
        in_raster="Dynamic_World_2022-0000065536-0000000000.tif",
        in_mask_data="Owan Watershed Boundary",
        extraction_area="INSIDE",
        analysis_extent='802434.418689543 737845.778255037 844343.858739178 791628.183061627 PROJCS["WGS_1984_UTM_Zone_31N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Owan_LULC")

# CLASSIFY LULC

# Reclassify LULC

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Owan_LULC",
        reclass_field="Value",
        remap="0 5;1 3;2 4;3 5;4 3;5 4;6 2;7 4;8 1",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC")




# Sediment Transport Index

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="STI",
        reclass_field="VALUE",
        remap="0 5 5;5 25 4;25 125 3;125 625 2",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_STI")





# WEIGHTED OVERLAY OWAN COMBINED

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 5 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN' 6 'Value' (3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order' 5 'Value' (1 1; 2 2; 3 3; 4 4; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Discharge' 5 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 7 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 5 'Value' (3 3; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 5 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 5 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Rainfall_2022' 5 'Value' (3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 5 'Value' (1 1; 2 2; 3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI' 7 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density' 5 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Power_Index' 5 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Slope' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Elevation' 10 'Value' (1 1; 2 2; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Combined")

# WEIGHTED OVERLAY OWAN SECOND DERIVATIVES

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN' 20 'Value' (3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order' 20 'Value' (1 1; 2 2; 3 3; 4 4; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density' 20 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Power_Index' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_2nd_Derivatives")

# CALCULATE ROC CURVES AND AUC VALUES (SECOND DERIVATIVES)

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_2nd_Derivatives",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)

# Weighted_Overlay_1st_Derivatives

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 9 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Discharge' 8 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 8 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 9 'Value' (3 3; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 9 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 9 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Rainfall_2022' 10 'Value' (3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Slope' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Elevation' 10 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 8 'Value' (1 1; 2 2; 3 3; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_1st_Derivatives")


# CALCULATE ROC CURVES AND AUC VALUES (FIRST DERIVATIVES)

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_1st_Derivatives",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)


# Weighted_Overlay_Owan_Technical

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN' 10 'Value' (3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order' 10 'Value' (1 1; 2 2; 3 3; 4 4; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Discharge' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Rainfall_2022' 10 'Value' (3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density' 10 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Power_Index' 10 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Slope' 15 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Elevation' 15 'Value' (1 1; 2 2; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Technical")


# Weighted_Overlay_Owan_Environmental

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 30 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 30 'Value' (3 3; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 40 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Environmental")

# Weighted_Overlay_Owan_Economic

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 50 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 50 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Economic")


# Weighted_Overlay_Owan_Social

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 50 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 50 'Value' (1 1; 2 2; 3 3; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Social")

# Weighted_Overlay_Owan_Technical_2

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Discharge' 25 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Rainfall_2022' 25 'Value' (3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Slope' 25 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Elevation' 25 'Value' (1 1; 2 2; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Technical_2")

# Weighted_Overlay_Owan_Sustainability

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 14 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 14 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 16 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 14 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 14 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 14 'Value' (1 1; 2 2; 3 3; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 14 'Value' (3 3; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Sustainability")

# Weighted_Overlay_Owan_Equitable

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 25 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 25 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 25 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 25 'Value' (1 1; 2 2; 3 3; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Equitable")


# Weighted_Overlay_Owan_Bearable

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_LULC' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 20 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 20 'Value' (3 3; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Population_Density' 20 'Value' (1 1; 2 2; 3 3; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Bearable")


# Weighted_Overlay_Owan_Viable

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Soil' 20 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Geology' 20 'Value' (3 3; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Protected_Ecological_Zone' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Road' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Distance_to_Settlement' 20 'Value' (1 1; 3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Weighted_Overlay_Owan_Viable")


# CALCULATE ROC CURVES AND AUC VALUES

# Technical

arcpy.ImportToolbox(r"C:\Users\fasip\Desktop\Study_Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="Hydropower_points",
    negative_points=None,
    model_rasters="Technical",
    dest_folder=r"C:\Users\f\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_ROC\2025_COMBINE_RESULTS_ROC"
)

# Economic

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Economic",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)

# Environmental

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Environmental",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)

# Social

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Social",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)



# Sustainability

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Sustainability",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)


# Equitable

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Equitable",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)


# Bearable

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Bearable",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)


# Viable

arcpy.ImportToolbox(r"C:\Users\f\Desktop\Study Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="power_potential_owan",
    negative_points=None,
    model_rasters="Weighted_Overlay_Owan_Viable",
    dest_folder=r"C:\Users\f\Desktop\Study Area\OWAN_SUB_BASIN\OWAN_ROC"
)

# Technical With STI
with arcpy.EnvManager(scratchWorkspace=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_STI' 16 'Value' (2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI' 17 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Power_Index' 17 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order' 17 'Value' (1 1; 2 2; 3 3; 4 4; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density' 17 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN' 16 'Value' (3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Technical_WSTI")

#Technical Without SPI

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.WeightedOverlay(
        in_weighted_overlay_table=r"('C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_STI' 20 'Value' (2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_TWI' 20 'Value' (1 1; 2 2; 3 3; 4 4; 5 5; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Stream_Order' 20 'Value' (1 1; 2 2; 3 3; 4 4; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_Drainage_Density' 20 'Value' (1 1; 2 2; NODATA NODATA); 'C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Reclass_Owan_CN' 20 'Value' (3 3; 4 4; 5 5; NODATA NODATA));1 5 1"
    )
    out_raster.save(r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\Technical_WTH_SPI")



# Protected Ecological Zone Map (Note: OKH Analysis)

#Reclassify PEZone

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study Area\OKHUNWAN\OKHUNWAN.gdb"):
    out_raster = arcpy.sa.Reclassify(
        in_raster="Okhunwan_Protected_Ecological_Zone_Raster",
        reclass_field="Value",
        remap="1 1",
        missing_values="DATA"
    )
    out_raster.save(r"C:\Users\f\Desktop\Study Area\OKHUNWAN\OKHUNWAN.gdb\Reclass_Okh_PEZone")

# OWAN ROC AUC Combined

arcpy.ImportToolbox(r"C:\Users\fasip\Desktop\Study_Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="Hydropower_points",
    negative_points=None,
    model_rasters="Social_2010;Social_2020;Economic;Environmental;Technical;Bearable;Bearable_2020;Equitable;Equitable_2020;Viable;Sustainability;Sustainability_2020",
    dest_folder=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_ROC\2025_COMBINE_RESULTS_ROC"
)

# Owan ROC AUC Technical and Technical_With_STI

arcpy.ImportToolbox(r"C:\Users\fasip\Desktop\Study_Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="Hydropower_points",
    negative_points=None,
    model_rasters="Technical_WSTI;Technical",
    dest_folder=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_ROC\2025_COMBINE_RESULTS_ROC"
)

# Owan Technical Plus STI Minus SPI

arcpy.ImportToolbox(r"C:\Users\fasip\Desktop\Study_Area\ArcSDM-master\ArcSDM-master\Toolbox\ArcSDM.pyt")
arcpy.ArcSDM.ROCTool(
    positive_points="Hydropower_points",
    negative_points=None,
    model_rasters="Technical_WTH_SPI;Technical",
    dest_folder=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_ROC\2025_COMBINE_RESULTS_ROC"
)


# Sediment Transport Index

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\f\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    output_raster = arcpy.sa.RasterCalculator(
        expression=' Power("Owan_Flow_Accumulation"/22.13,0.6) * Power( Sin("Owan_Slope"/0.0896),1.3)'
    )
    output_raster.save(r"C:\Users\f\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\RasterC_1")









Focal Statistics for Reclass STI (Spatial Analyst)

with arcpy.EnvManager(scratchWorkspace=r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb"):
    out_raster = arcpy.sa.FocalStatistics(
        in_raster="Reclass_STI",
        neighborhood="Rectangle 3 3 CELL",
        statistics_type="MEAN",
        ignore_nodata="DATA",
        percentile_value=90
    )
    out_raster.save(r"C:\Users\fasip\Desktop\Study_Area\OWAN_SUB_BASIN\OWAN_SUB_BASIN.gdb\FocalSt_ReclassSTI")