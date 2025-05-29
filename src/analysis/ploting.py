# my improts
from src.data_extraction.jsonhandling import JsonHandling
from src.sim_gui import SimulateGui

# other imports
import  matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import polars as pl
import numpy as np
#import dataframe_image as dfi

class PlotingAnalysis:


    def plot_stints(df_stints: pl.DataFrame) -> None:
        """
            Args:
                df_stints (pl.DataFrame) - combined df of df_drivers and df_stints
            Returns:
                None
            Plots horizontal bar graph for every driver in the given session, graph color is based on the tyre compound 
        """
        fig, ax = plt.subplots()
        for name in df_stints["name"]:
           df = df_stints.filter(df_stints["name"] == name)
           for index,num in enumerate(df["stint_number"]):
                lap_start = df[index]["lap_start"][0]
                lap_end = df[index]["lap_end"][0]
                lap_duration = lap_end - lap_start
                driver_name = df[index]["name"][0]
                compound = df[index]["compound"][0]

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
        plt.savefig("images_for_sending/stints.png", bbox_inches='tight', dpi=300)
        plt.close()
        #plt.show()

    def plot_fastest_secotors(df_fastest_sectors: pl.DataFrame) -> None:
        data = df_fastest_sectors.rows()
        columns = df_fastest_sectors.columns

        fig, ax = plt.subplots()
        ax.axis('off')  

        table = ax.table(cellText=data, colLabels=columns, loc='center')
        print(table)
        plt.savefig("images_for_sending/fastest_sectors_and_fastest_lap.png", bbox_inches='tight', dpi=300)
        plt.close()

    def plot_average_for_stints(df_average_for_stints) -> None:
        data = df_average_for_stints.rows()
        #data = data.values.tolist()
        columns = df_average_for_stints.columns

        fig, ax = plt.subplots()
        ax.axis('off')  

        table = ax.table(cellText=data, colLabels=columns, loc='center')
        print(table)
        plt.savefig("images_for_sending/average_for_stints.png", bbox_inches='tight', dpi=300)
        plt.close()

    def plot_car_data(df_list_speed, df_list_lap_number_and_start_date):
        plt.figure(figsize=(13, 8))
        lap_numbers = df_list_lap_number_and_start_date[0].height
        lap = SimulateGui.select_lap_for_car_data_analysis(lap_numbers)
        
        for num,driver in enumerate(df_list_speed):
            start = df_list_lap_number_and_start_date[num].row(lap-1)[df_list_lap_number_and_start_date[num].columns.index("date_start")]
            end = df_list_lap_number_and_start_date[num].row(lap)[df_list_lap_number_and_start_date[num].columns.index("date_start")]

            driver = driver.filter(driver['date'] <= end)
            driver = driver.filter(driver['date'] >= start)
            speeds = driver["speed"].to_numpy()
            driver_name = driver["name"].to_numpy()[0]

            times = times = np.arange(len(driver['date']))
            plt.plot(times, speeds, label=driver_name)

        plt.title("Driver Speed Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (km/h)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

            

