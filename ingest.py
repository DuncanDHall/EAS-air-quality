import numpy as np
import pandas as pd

import os
from io import StringIO

heads = {
    'RD':"RD|Action Code|State Code|County Code|Site ID|Parameter|POC|Sample Duration|Unit|Method|Date|Start Time|Sample Value|Null Data Code|Sampling Frequency|Monitor Protocol (MP) ID|Qualifier - 1|Qualifier - 2|Qualifier - 3|Qualifier - 4|Qualifier - 5|Qualifier - 6|Qualifier - 7|Qualifier - 8|Qualifier - 9|Qualifier - 10|Alternate Method Detectable Limit|Uncertainty",
    'RC':"RC|Action Code|State Code|County Code|Site ID|Parameter|POC|Unit|Method|Year|Period|Number of Samples|Composite Type|Sample Value|Monitor Protocol (MP) ID|Qualifier - 1|Qualifier - 2|Qualifier - 3|Qualifier - 4|Qualifier - 5|Qualifier - 6|Qualifier - 7|Qualifier - 8|Qualifier - 9|Qualifier - 10|Alternate Method Detectable Limit|Uncertainty",
    '1':"SITE INFORMATION TYPE = 1|STATE_CODE|STATE_NAME|COUNTY_CODE|COUNTY_NAME|SITE_ID|PARAMETER_CODE|PARAMETER_DESC|CITY_CODE|CITY_NAME|STREET_ADDRESS|AQCR_CODE|AQCR_NAME|CBSA_CODE|CBSA_NAME|CSA_CODE|CSA_NAME|EPA_REGION|UAR_CODE|UAR_NAME|LAND_USE|LOC_SET|LATITUDE|LONGITUDE|UTM_ZONE|UTM_NORTHING|UTM_EASTING|HORIZ_COLLECT|HORIZ_METHOD|HORIZ_DATUM|HORIZ_ACC|HORIZ_SCALE|ELEVATION_MSL|VERT_COLLECT|VERT_METHOD|VERT_DATUM|VERT_ACC",
    '2':"DAILY VALUE TYPE = 2|STATE_CODE|COUNTY_CODE|SITE_ID|PARAMETER_CODE|UNITS|PRIMARY_MONITOR_POC|MONITOR_TYPE|PQAO|PQAO_NAME|SAMPLE_DATE|VALUE|SOURCE|EDT_ID"
}

# Functionize everything!
def load_split_file(file):
    with open(file) as f:
        lines1 = pd.DataFrame(f.readlines(),columns=['raw'])
    
    lines1['comment']=[s.startswith('#') for s in lines1.raw]
    lines1['type']=[s.split('|')[0] for s in lines1.raw]
    
    # Drop comment lines
    lines1.drop(lines1[lines1.comment].index, inplace=True)
    lines1.tail()
    
    # Split into row types
    types=lines1.type.unique()
    outputs = dict()
    for t in types:
        if t not in heads:
            raise Exception('Unknown row type '+t)
        outputs[t] = StringIO(heads[t]+'\n'+''.join(lines1[lines1.type==t].raw))

    return outputs