#my class imports
from src.data_extraction.cached_api_extraction.stint_API import Stint
from src.data_extraction.cached_api_extraction.drivers_API import DriversApi
from src.data_extraction.cached_api_extraction.laps_API import Laps

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Analysis:


    def __init__(self, session, meeting):
        self.session = session
        self.meeting = meeting

    def stints(self, setparam: object):
        """
            Args:
                setparam (:obj:) - instance of SetParam class
            Output:
                Plots stints for all the drivers depending on the choosen session
        """
        df_drivers = DriversApi.get_df_drivers(setparam)
        df_stints = Stint.get_df_stints(self.session)
        
        df_combined = df_stints.join(df_drivers, left_on="driver_number", right_on="number", how="inner")

        fig, ax = plt.subplots()
        for name in df_drivers["name"]:
           driver_df = df_combined.filter(df_combined["name"] == name)
           for index,num in enumerate(driver_df["stint_number"]):
                lap_start = driver_df[index]["lap_start"][0]
                lap_end = driver_df[index]["lap_end"][0]
                lap_duration = lap_end - lap_start
                driver_name = driver_df[index]["name"][0]
                compound = driver_df[index]["compound"][0]

                if compound == "SOFT":
                   color = "red"
                elif compound == "MEDIUM":
                   color = "orange"
                elif compound == "HARD":
                   color = "gray"

                p1 = plt.barh(driver_name, lap_duration+1, left=lap_start,
                         color=color, edgecolor="black")
                ax.bar_label(p1, label_type='center')
                
        tier_compound = ["Soft", "Medium", "Hard"]
        tier_color = ["red", "orange", "gray"]
        legend_handles = [mpatches.Patch(color=color, label=label) for color, label in zip(tier_color, tier_compound)]

        plt.xlabel("Laps")
        plt.title("Race Stints")
        plt.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        plt.show()
    
    def drivers_lap_time(self, setparam: object, driver_num: int):
        df_drivers = DriversApi.get_df_drivers(setparam)
        df_laps = Laps.get_single_df_laps(setparam.session_key, driver_num)
        df_combined = df_laps.join(df_drivers, left_on="driver_number", right_on="number", how="inner")
        print(df_combined)
        all_laps_duration = df_combined.select(df_combined["lap_duration"])
        print(all_laps_duration)
        average_lap_time = all_laps_duration[1:].sum()/len(all_laps_duration[1:])
        print(all_laps_duration[1:].sum(), len(all_laps_duration[1:]))
        print(average_lap_time)


                

