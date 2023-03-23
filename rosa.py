# file: rosa.py
# authors:
#           -Jorge Alejandro Rodríguez Aldana
#           -Josué Daniel Cuzco Rivera
# date: 2023-03-16

import numpy as np
import pandas as pd

def get_angle_diff_and_mean(angle_1:float,angle_2:float) -> tuple:
    """Returns the min difference between angles and its mean inside this arc.

    Parameters
    ----------
    angle_1 : float
        Angle between 0 and 360
    angle_2 : float
        Angle between 0 and 360

    Returns
    -------
    tuple
        Minimun difference between angles; Angle between angles.
    """
    angles = [angle_1,angle_2]
    min_angle = min(angles)
    diff = abs(angle_1-angle_2)
    mean_angle = min_angle + (diff/2)

    if diff > 180:
        mean_angle += 180
        diff = 360 - diff
    
    mean_angle = mean_angle % 360

    if mean_angle == 0:
        mean_angle = 360

    return diff, mean_angle

def get_name_from_degree(angle:float) -> int:
    """Return the int name from the calculated angle

    Parameters
    ----------
    angle : float
        Angle you want to set into the discretization

    Returns
    -------
    int
        Discretizated angle
    """
    if (angle > 22.5) and (angle <= 67.5):
        predo=45
    if (angle > 67.5) and (angle <= 112.5):
        predo=90
    if (angle > 112.5) and (angle <= 157.5):
        predo=135
    if (angle > 157.5) and (angle <= 202.5):
        predo=180
    if (angle > 202.5) and (angle <= 247.5):
        predo=225
    if (angle > 247.5) and (angle <= 292.5):
        predo=270
    if (angle > 292.5) and (angle <= 337.5):
        predo=315
    if (angle > 337.5) and (angle <= 360):
        predo=360
    if (angle >0) and (angle <= 22.5):
        predo=360
    return predo

def get_degree_value(angle_1:float,angle_2:float,angle_3:float) -> tuple:
    """Returns the angle following the wind rose procedure.

    Parameters
    ----------
    angle_1 : float
        Angle between 0 and 360
    angle_2 : float
        Angle between 0 and 360
    angle_3 : float
        Angle between 0 and 360

    Returns
    -------
    tuple
        Tuple containing the following:
        * Angle following the wind rose procedure
        * Discretized angle
    """

    if not (0 <= angle_1 <= 360):
        angle_1 = np.nan
    if not (0 <= angle_2 <= 360):
        angle_2 = np.nan
    if not (0 <= angle_3 <= 360):
        angle_3 = np.nan
        
    angles_list = [angle_1,angle_2,angle_3]

    def three_angles(angle_1,angle_2,angle_3) -> float:

        num2angle = {1:angle_1,2:angle_2,3:angle_3}

        diffs_means = []
        diffs_means.append([get_angle_diff_and_mean(angle_1,angle_2),{1,2}])
        diffs_means.append([get_angle_diff_and_mean(angle_1,angle_3),{1,3}])
        diffs_means.append([get_angle_diff_and_mean(angle_2,angle_3),{2,3}])

        diffs_means.sort()

        # print(diffs_means)
        # return diffs_means

        if diffs_means[0][0][0] >= 90:
            return 9,9
        
        if diffs_means[0][0][0] == diffs_means[1][0][0]:
            angle_num = list(diffs_means[0][1] & diffs_means[1][1])[0]
            return num2angle[angle_num],get_name_from_degree(num2angle[angle_num])
        
        return diffs_means[0][0][1],get_name_from_degree(diffs_means[0][0][1])

    def two_angles(angle_1,angle_2):
        diff, mean_angle = get_angle_diff_and_mean(angle_1,angle_2)

        # print(diff,mean_angle)

        if diff >= 90:
            return 9,9
        else:
            return mean_angle,get_name_from_degree(mean_angle)

    if np.nan in angles_list:
        return np.nan, np.nan
    
    else:

        if 0 in angles_list:
            if angles_list.count(0) > 1:
                return 0,0
            else:
                if 9 in angles_list:
                    return 9,9
                else:
                    angles_list.remove(0)
                    return two_angles(angles_list[0],angles_list[1])
        
        elif 9 in angles_list:
            if angles_list.count(9) > 1:
                return 9,9
            else:
                angles_list.remove(9)
                return two_angles(angles_list[0],angles_list[1])
            
        else:
            return three_angles(angle_1,angle_2,angle_3)
                
def get_df_column(df:pd.DataFrame,colnames = ['dir_viento_7:00','dir_viento_13:00','dir_viento_18:00']) -> pd.Series:
    """Generates a pandas.core.series.Series object with the contents of a column of the input DataFrame based on the three columns passed on colnames.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame
    colnames : list, optional
        List of names asociated with the three angles columns in the DataFrame, by default ['dir_viento_7:00','dir_viento_13:00','dir_viento_18:00']

    Returns
    -------
    pd.Series
        Returns a Series object which you can asociate with the original dataframe as follows:

        ```python
        import pandas as pd
        import rosa

        df:pd.DataFrame

        df['dir_final'] = get_df_column(df)
        ```
    """
    dir_final = df.apply(lambda row: get_degree_value(row[colnames[0]],row[colnames[1]],row[colnames[2]])[1],axis=1)
    return dir_final

