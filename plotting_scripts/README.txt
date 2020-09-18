This contains all of the scripts to reproduce the figures in Penn & Holloway 2020. 

--------------------------
 monitor_comparison.ipynb
--------------------------
-Produces Figures 1, 2, and 3. 
-Requires daily gridded GOME-2 and OMI files from WHIPS. These are contained in the folder WHIPS-output. See the README in this folder for more information. 

--------------------------------
 plot_monthly_average_sat.ipynb
--------------------------------
-Produces Figure 4.
-Requires GOME-2 and OMI files averaged by months, or several months. These are contained in the folder level3data. 
-To produce these files from daily gridded WHIPS files, use the average_0_25_gome2_omi.py and average_0_5_gome2_omi.py scripts. 

--------------------------------------------------------
 average_0_5_gome2_omi.py and average_0_25_gome2_omi.py
--------------------------------------------------------
-Produced monthly- or summer- averaged files from daily gridded WHIPS output. 
-For each day, only includes grid cells where *both* GOME-2 and OMI have a valid measurement. 
-You can specify the date range you want to average over in this file. 