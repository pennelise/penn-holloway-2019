The folder WHIPS-output contains gridded NO2 concentrations processed by WHIPS: https://github.com/WHIPS-team/WHIPS3. I used the OMNO2d gridding algorithm, which is currently only available in the gome2 branch. 

Each folder also contains a sample WHIPS script (titled in the format 'whips_*.py') used for obtaining 1 month of data. 

List of files available:

---------------------------
0_25x0_25_CONUS_gridfile.nc
---------------------------
This file specifies where the corners and centers of the grid cells are for data gridded by WHIPS onto a 0.25°x0.25° grid over the US. It is included at the top of this directory, as well as within the folder for every 0.25°x0.25° product. It is identical for each of these products, however. 

------------------------- 
0_5x0_5_CONUS_gridfile.nc 
-------------------------
This file specifies where the corners and centers of the grid cells are for data gridded by WHIPS onto a 0.5°x0.5° grid over the US. It is included at the top of this directory, as well as within the folder for every 0.5°x0.5° product. It is identical for each of these products, however. 


List of folders available: 

---------------------
DOMINO/grid_0_25x0_25
---------------------
DOMINO observations for June-August 2007. 
Gridded on a 0.25°x0.25° grid.
Each file represents 1 day of DOMINO observations.   

------------------
DOMINO/grid0_5x0_5
------------------
DOMINO observations for June-August 2007. 
Gridded on a 0.5°x0.5° grid.
Each file represents 1 day of DOMINO observations.   

------------------
DOMINO/cloudfrac_0
------------------
DOMINO observations for June-August 2007. 
Gridded on a 0.25°x0.25° grid.
Each file represents 1 day of DOMINO observations.   
Only files with no clouds at all (cloudfrac=0) were allowed here. 

----------------------------------
GOME2/grid_0_25x0_25_no_big_pixels
----------------------------------
GOME2 observations for June-August 2007.
Gridded on a 0.25°x0.25° grid.
Each file represents 1 day of GOME2 observations.
Only pixels smaller than 5800km^2 were used. There are some extremely large pixels (up to 15500km^2) included in GOME-2 data. I do not know why they are there. You may choose to include them. 

-------------------------------
GOME2/grid0_5x0_5_no_big_pixels
-------------------------------
GOME2 observations for June-August 2007.
Gridded on a 0.5°x0.5° grid.
Each file represents 1 day of GOME2 observations.
Only pixels smaller than 5800km^2 were used. There are some extremely large pixe
ls (up to 15500km^2) included in GOME-2 data. I do not know why they are there.
You may choose to include them. 

-----------------
GOME2/cloudfrac_0
-----------------
GOME2 observations for June-August 2007.
Gridded on a 0.25°x0.25° grid.
Each file represents 1 day of GOME2 observations.
Only files with no clouds at all (cloudfrac=0) were allowed here. 
