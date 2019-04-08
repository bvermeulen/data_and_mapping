'''' Dict of PSS attributes 
     Each attribute has following dicts:
     :col: column in csv
     :range: range of values pss data has to be within
     :min: minimum value for color bar
     :max: maximum valuw for color bar
     :title: general description of attribute
'''

pss_attr = {'Encoder Index': {'col':0, 'range': None, 'min': None, 'max': None, 'title': None},
            'Void': {'col': 1, 'range': None, 'min': None, 'max': None, 'title': None},
            'Shot ID': {'col': 2, 'range': None, 'min': None, 'max': None, 'title': None},
            'File Num': {'col': 3, 'range': None, 'min': None, 'max': None, 'title': None},
            'EP ID': {'col': 4, 'range': None, 'min': None, 'max': None, 'title': None},
            'Line': {'col': 5, 'range': None, 'min': None, 'max': None, 'title': None},
            'Station': {'col': 6, 'range': None, 'min': None, 'max': None, 'title': None},
            'Date': {'col': 7, 'range': None, 'min': None, 'max': None, 'title': None},
            'Time': {'col': 8, 'range': None, 'min': None, 'max': None, 'title': None},
            'Comment': {'col': 9, 'range': None, 'min': None, 'max': None, 'title': None},
            'TB Date': {'col': 10, 'range': None, 'min': None, 'max': None, 'title': None},
            'TB Time': {'col': 11, 'range': None, 'min': None, 'max': None, 'title': None},
            'TB Micro': {'col': 12, 'range': None, 'min': None, 'max': None, 'title': None},
            'Record Index': {'col': 13, 'range': None, 'min': None, 'max': None, 'title': None},
            'EP Count': {'col': 14, 'range': None, 'min': None, 'max': None, 'title': None},
            'Crew ID': {'col': 15, 'range': None, 'min': None, 'max': None, 'title': None},
            'Unit ID': {'col': 16, 'range': None, 'min': None, 'max': None, 'title': None},
            'Start Code': {'col': 17, 'range': None, 'min': None, 'max': None, 'title': None},
            'Sweep Checksum': {'col': 18, 'range': None, 'min': None, 'max': None, 'title': None},
            'Param Checksum': {'col': 19, 'range': None, 'min': None, 'max': None, 'title': None},
            'Phase Max': {'col': 20, 'range': 3, 'min': 0, 'max': 10, 'title': 'Peak phase'},
            'Phase Avg': {'col': 21, 'range': 3, 'min': 0, 'max': 5, 'title': 'Average phase'},
            'Force Max': {'col': 22, 'range': 10, 'min': 0, 'max': 100, 'title': 'Peak force'},
            'Force Avg': {'col': 23, 'range': 10, 'min': 20, 'max': 80, 'title': 'Average force'},
            'THD Max': {'col': 24, 'range': 5, 'min': 0, 'max': 40, 'title': 'Peak distortion'},
            'THD Avg': {'col': 25, 'range': 5, 'min': 0, 'max': 20, 'title': 'Average distortion'},
            'Force Out': {'col': 27, 'range': 10, 'min': 0, 'max': 100, 'title': 'Output force'},
            'GPS Time': {'col': 27, 'range': None, 'min': None, 'max': None, 'title': None},
            'Lat': {'col': 28, 'range': None, 'min': None, 'max': None, 'title': None},
            'Lon': {'col': 29, 'range': None, 'min': None, 'max': None, 'title': None},
            'Altitude': {'col': 30, 'range': 10, 'min': 200, 'max': 300, 'title': 'Elevation'},
            'GPS Altitude': {'col': 31, 'range': None, 'min': None, 'max': None, 'title': None},
            'Sats': {'col': 32, 'range': None, 'min': None, 'max': None, 'title': None},
            'PDOP': {'col': 33, 'range': None, 'min': None, 'max': None, 'title': None},
            'HDOP': {'col': 34, 'range': None, 'min': None, 'max': None, 'title': None},
            'VDOP': {'col': 35, 'range': None, 'min': None, 'max': None, 'title': None},
            'Age': {'col': 36, 'range': None, 'min': None, 'max': None, 'title': None},
            'Quality': {'col': 37, 'range': None, 'min': None, 'max': None, 'title': None},
            'Start Time Delta': {'col': 38, 'range': None, 'min': None, 'max': None, 'title': None},
            'Sweep Number': {'col': 39, 'range': None, 'min': None, 'max': None, 'title': None},
            'Signature File Number': {'col': 40, 'range': None, 'min': None, 'max': None, 'title': None},
            'Flash Storage Free Spac': {'col': 41, 'range': None, 'min': None, 'max': None, 'title': None},
            'Flash Storage Status': {'col': 42, 'range': None, 'min': None, 'max': None, 'title': None},
            'USB Storage Status': {'col': 43, 'range': None, 'min': None, 'max': None, 'title': None},
            'Vibrator QC': {'col': 44, 'range': None, 'min': None, 'max': None, 'title': None},
            'Encoder ID': {'col': 45, 'range': None, 'min': None, 'max': None, 'title': None},
            'Encoder IP': {'col': 46, 'range': None, 'min': None, 'max': None, 'title': None},
            'Max Viscosity': {'col': 47, 'range': 30, 'min': None, 'max': None, 'title': 'Max viscosity'},
            'Min Viscosity': {'col': 48, 'range': 30, 'min': None, 'max': None, 'title': 'Min viscosity'},
            'Avg Viscosity': {'col': 49, 'range': 30, 'min': None, 'max': None, 'title': 'Viscosity'},
            'Max Stiffness': {'col': 50, 'range': 5, 'min': None, 'max': None, 'title': 'Max stiffness'},
            'Min Stiffness': {'col': 51, 'range': 5, 'min': None, 'max': None, 'title': 'Min stiffness'},
            'Avg Stiffness': {'col': 52, 'range': 5, 'min': 0, 'max': 20, 'title': 'Stiffness'},
            'Target Force': {'col': 53, 'range': 10, 'min': 0, 'max': 100, 'title': 'Target force'},
            'Bearing': {'col': 54, 'range': None, 'min': None, 'max': None, 'title': None},  # not consistent
           }