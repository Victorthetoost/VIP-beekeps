#add a new beehive to the compiled dataset
import pandas as pd

# if ti already exists in the compiled dataset, add to the end of it's section, if not, add it to the end of the dataset
#search for the beehive in the compiled dataset
compiled_data = pd.read_csv("compiled_beehive_data.csv")

def process_new_data(new_data, empty_C, empty_E):
    new_data["Difference In Temperature From Empty Center"] = round(new_data["Temperature_Fahrenheit"] - empty_C["Temperature_Fahrenheit"],3)
    new_data["Difference In Temperature From Empty Edge"] = round(new_data["Temperature_Farenheit_Edge"] - empty_E["Temperature_Fahrenheit"],3) 
    new_data["Difference In Humidity From Empty Center"] = round(new_data["Relative_Humidity"] - empty_C["Relative_Humidity"],3) 
    new_data["Difference In Humidity From Empty Edge"] = round(new_data["Relative_Humidity_Edge"] - empty_E["Relative_Humidity"],3)
    return new_data

def insert_new_data(compiled_data, new_data, beehive):
    if beehive in compiled_data["Name"].values:
        #if it exists, insert it in the correct place
        index = compiled_data[compiled_data["Name"] == beehive].index[-1] + 1
        #insert the new data at the correct index
        compiled_data = pd.concat([compiled_data.iloc[:index], new_data, compiled_data.iloc[index:]]).reset_index(drop=True)
    else:
        #if it doesn't exist, add it to the end of the dataset
        compiled_data = pd.concat([compiled_data, new_data], ignore_index=True)

    compiled_data.to_csv("compiled_beehive_data.csv", index=False)

def death_timestamp(beehive_data, timestamp):
    #selects a timestap for when that hive died, and labels all the timestamps after that as dead, and all the timestamps before that as alive.
    # if there isnt a timestamp, assume all alive
    if timestamp is not None:
        beehive_data["Alive_or_Dead"] = beehive_data["Timestamp"].apply(lambda x: 1 if x < timestamp else 0)
    else:
        beehive_data["Alive_or_Dead"] = 1
    return beehive_data


if __name__ == "__main__":
#files and whatnot
    filename = "Beehive_export_adjfkhadkjlfhkl.csv"
    beehive = filename.split("_")[0]
    new_data = pd.read_csv(filename)
    empty_C = pd.read_csv("data/Sensor C_export_202512201200.csv")
    empty_E = pd.read_csv("data/Sensor E_export_202512201200.csv")
    death_timestamp = None #format: "2026-01-01 00:00:00" hour min second.
    #none means that it is alive (and well(?))

    #implement
    new_data = process_new_data(new_data, empty_C, empty_E)
    new_data = death_timestamp(new_data, death_timestamp) 
    insert_new_data(compiled_data, new_data, beehive)

