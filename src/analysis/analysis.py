# my imports
from src.data_extraction.cached_api_extraction.stint_API import Stint
from src.data_extraction.cached_api_extraction.drivers_API import DriversApi
from src.data_extraction.cached_api_extraction.laps_API import LapsAPI
from src.data_extraction.jsonhandling import JsonHandling
from src.data_extraction.cached_api_extraction.cardata_API import CarData
from src.data_extraction.cached_api_extraction.sessions_API import SessionAPi
 
# other imports

import polars as pl


class Analysis:
    """Class for general analysis"""

    def __init__(self, session, meeting):
        self.session = session
        self.meeting = meeting

    def stints(self, setparam: object):
        """
            Args:
                setparam (:obj:) - instance of SetParam class
            Return:
                Dataframe that combines drivers number with their stint
        """
        df_drivers = DriversApi.get_df_drivers(setparam)
        df_stints = Stint.get_df_stints(self.session)
        
        df_combined = df_stints.join(df_drivers, left_on="driver_number", right_on="number", how="inner")
        return df_combined
        
    
    def all_drivers_fastest_sectors(self, setparam: object) -> pl.DataFrame:
        """
            Args:
                setparam (:obj:) - Class that holds all the set parameters 
            Return:
                Returns dic that holds all drivers fastest sectors(they are 99% not from the same lap)"""
        
        df_drivers = DriversApi.get_df_drivers(setparam)   
        df_laps = LapsAPI.get_df_laps(setparam.session_key)
        df_combined = df_laps.join(df_drivers, left_on="driver_number", right_on="number", how="inner")
        
        df_combined = df_combined.select(   df_combined["lap_duration"],
                                            df_combined['duration_sector_1'],
                                            df_combined['duration_sector_2'],
                                            df_combined['duration_sector_3'],
                                            df_combined["name"],
                                         )    
        
        dic_fastest_sectors = []    
        for name in df_drivers["name"]:
            temp_dic = {}
            df = df_combined.filter(df_combined["name"] == name)
            driver_name = name
            filtered_df = df.filter(
                pl.col("duration_sector_1").is_not_null() &
                pl.col("duration_sector_2").is_not_null() &
                pl.col("duration_sector_3").is_not_null()
                                    )               
            temp_dic["name"] = driver_name
            temp_dic["fastest sector 1"] = min(filtered_df["duration_sector_1"])
            temp_dic["fastest sector 2"] = min(filtered_df["duration_sector_2"])
            temp_dic["fastest sector 3"] = min(filtered_df["duration_sector_3"])
            temp_dic["fastest lap"] = min(filtered_df["lap_duration"])
            dic_fastest_sectors.append(temp_dic)
        df_fastest_sectors = pl.DataFrame(dic_fastest_sectors)
        df_fastest_sectors = df_fastest_sectors.sort("fastest lap")
        print(df_fastest_sectors)
        return df_fastest_sectors

    def car_data(self, drivers: list[dict], setparam: object) -> pl.DataFrame:
        """
            Args:
                drivers (list[dict]) - drivers that where selected for their cardata analysis
                setparam (:object:) - class object where are loaded all the parameters needed for the session
            Return:
                Return a data frame which holds speed and the point in time when that speed was measured and name of the driver
        """
        df_laps = LapsAPI.get_df_laps(setparam.session_key)
        df_drivers = DriversApi.get_df_drivers(setparam)
        df_list_cardata = CarData.get_df_cardata(drivers, setparam)
        df_session_data = SessionAPi.get_df_session(setparam)
        #print(df_laps, df_drivers, df_list_cardata, df_session_data)

        df_session_data = df_session_data.filter(df_session_data["session_key"] == setparam.session_key)
        #print(df_session_data)

        df_list_speed = []
        for num in range(len(df_list_cardata)):
            df = df_list_cardata[num].join(df_drivers, left_on="driver_number", right_on="number", how="inner")
            #print(df['name'])
            df_list_speed.append(df.select( df['speed'],
                                            df['name'],
                                            df['date'],
                                          ) 
                                )
        df_list_lap_number_and_start_date = []
        for driver in drivers:
            df = df_laps.filter(df_laps['driver_number'] == driver['number'])
            df = df.select(   df["lap_number"],
                                        df['date_start'],
                                        )
            #fillinf for the first lap since there is no date_start for that lap, needs to be filled from session
            df = df.with_columns(
                pl.col("date_start")
                .fill_null(df_session_data["date_start"])
                .alias("date_start")
                                )
            df_list_lap_number_and_start_date.append(df) 
            #print("AAAAAAAAAAAAAAAAAAAAAAaaa", df_list_lap_number_and_start_date)
        return df_list_speed, df_list_lap_number_and_start_date

        
    
class Race(Analysis):


    def __init__(self, session, meeting):
        super().__init__(session, meeting)
    
    def average_driver_lap_time(self, setparam: object, driver_list: list[int]):
        for driver in driver_list:
            df_drivers = DriversApi.get_df_drivers(setparam)
            df_laps = LapsAPI.get_single_df_laps(setparam.session_key, driver)
            df_combined = df_laps.join(df_drivers, left_on="driver_number", right_on="number", how="inner")

           
            all_laps_duration = df_combined.select(df_combined["lap_duration"])
            print(all_laps_duration)
            average_lap_time = all_laps_duration[1:].sum()/len(all_laps_duration[1:])
            #print(all_laps_duration[1:].sum(), len(all_laps_duration[1:]))
            print(average_lap_time)
         
    def all_drivers_average_times_per_stint(self, setparam: object): 
        df_drivers = DriversApi.get_df_drivers(setparam) 
        df_laps = LapsAPI.get_df_laps(setparam.session_key) 
        df_combined = df_laps.join(df_drivers, left_on="driver_number", right_on="number", how="inner")
        print(df_combined.columns)
        df_combined = df_combined.select(   
                                            df_combined['name'],
                                            df_combined["lap_duration"],
                                            df_combined["is_pit_out_lap"],
                                            df_combined['duration_sector_1'],
                                            df_combined['duration_sector_2'],
                                            df_combined['duration_sector_3'],
                                       )
        
        rows = []
        for name in df_drivers["name"]:
            df_filtered = df_combined.filter(df_combined["name"] == name)
            
            df_filtered = df_filtered.filter(
                pl.col("duration_sector_1").is_not_null() &
                pl.col("duration_sector_2").is_not_null() &
                pl.col("duration_sector_3").is_not_null()
                                    )
            start = 0
            stint = 1
            for num,in_pit in enumerate(df_filtered["is_pit_out_lap"]):
                #print(num, in_pit)
                if in_pit == True or num == len(df_filtered["is_pit_out_lap"])-1:
                    
                    driver_name = df_filtered["name"][0]

                    column_laps = df_filtered.select(df_filtered["lap_duration"])
                    sector_1 = df_filtered.select(df_filtered["duration_sector_1"])
                    sector_2 = df_filtered.select(df_filtered["duration_sector_2"])
                    sector_3 = df_filtered.select(df_filtered["duration_sector_3"])

                    average_lap_time = round((column_laps[start:num].sum() / len(column_laps[start:num])).item(), 3)
                    average_sector_1 = round((sector_1[start:num].sum() / len(sector_1[start:num])).item(), 3)
                    average_sector_2 = round((sector_2[start:num].sum() / len(sector_2[start:num])).item(), 3)
                    average_sector_3 = round((sector_3[start:num].sum() / len(sector_3[start:num])).item(), 3)

                    row = {
                        "name": driver_name,
                        "stint":  stint,
                        "average lap time": average_lap_time,   
                        "average sector 1": average_sector_1,   
                        "average sector 2": average_sector_2,   
                        "average sector 3": average_sector_3,   
                    }
                    rows.append(row) 
                
                    start = num
                    stint += 1
        final_df = pl.DataFrame(rows) 
        sorted_df  = final_df.sort("average lap time") 
        print(final_df)
        print(JsonHandling.pretty_json(rows))
        return sorted_df
    


class Qualifying(Analysis):
    def __init__(self, session, meeting):
        super().__init__(session, meeting)

    def qually_placing():
        pass

            
            


        



                

