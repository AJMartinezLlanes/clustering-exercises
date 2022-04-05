import pandas as pd
import numpy as np
import os

from env import get_db_url
from sklearn.model_selection import train_test_split    
 
import warnings
warnings.filterwarnings("ignore")


# Function to get zillow data
def get_zillow_data():    
    filename = 'zillow.csv'
    if os.path.exists(filename):
        print('Reading from csv file...')
        return pd.read_csv(filename)
      
    query= '''
    SELECT prop.*,
	pred.logerror,
	pred.transactiondate,	
	cons.typeconstructiondesc,
	air.airconditioningdesc,
	arch.architecturalstyledesc,
	build.buildingclassdesc,
	land.propertylandusedesc,		
	story.storydesc
	
    FROM properties_2017 prop
	    INNER JOIN(SELECT parcelid, logerror, MAX(transactiondate)transactiondate
				  FROM predictions_2017
				  GROUP BY parcelid, logerror) pred
			USING (parcelid)
	    LEFT JOIN typeconstructiontype cons USING (typeconstructiontypeid)
	    LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
	    LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
	    LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
	    LEFT JOIN propertylandusetype land USING (propertylandusetypeid)
	    LEFT JOIN storytype story USING (storytypeid)
    WHERE prop.latitude IS NOT NULL
	    AND prop.longitude IS NOT NULL
	    AND transactiondate LIKE '2017%%';
    '''
    print('Getting a fresh copy from SQL database...')
    df = pd.read_sql(query, get_db_url('zillow'))
    print('Saving to csv...')
    df.to_csv(filename, index=False)
    return df

