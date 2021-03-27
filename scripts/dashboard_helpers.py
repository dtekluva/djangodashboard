# from main.models import Datalog
import pandas as pd
from . import remote_request
import json
### FOR TEMPLATE RENDERING
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import random, os
from datetime import datetime

frequencies = {
        "15mins": "15T",
        "30mins": "30T",
        "hourly": "1h",
        "daily": "D",
        "weekly": "W-SAT",
        "monthly": "M",
    }    

def get_diesel_consumption_rate(gen_size, load):

    consumption_by_size =  {
                            10:{
                                    0.25: 0.9,
                                    0.5: 1.2,
                                    0.75: 1.7,
                                    1.0:2.1
                            },
                            12:{
                                    0.25: 1.0,
                                    0.5: 1.4,
                                    0.75: 2.1,
                                    1.0:2.6
                            },
                            15:{
                                    0.25: 1.3,
                                    0.5: 1.8,
                                    0.75: 2.6,
                                    1.0:3.2
                            },
                            20:{
                                    0.25: 1.7,
                                    0.5: 2.4,
                                    0.75: 3.5,
                                    1.0:4.3
                            },
                            25:{
                                    0.25: 2.1,
                                    0.5: 3.0,
                                    0.75: 4.3,
                                    1.0:5.4
                            },
                            30:{
                                    0.25: 2.6,
                                    0.5: 3.6,
                                    0.75: 5.2,
                                    1.0:6.4
                            },
                            40:{
                                    0.25: 3.4,
                                    0.5: 4.8,
                                    0.75: 7.0,
                                    1.0:8.6
                            },
                            50:{
                                    0.25: 4.3,
                                    0.5: 6.0,
                                    0.75: 8.6,
                                    1.0:10.7
                            },
                            75:{
                                    0.25: 6.4,
                                    0.5: 9.0,
                                    10.75: 2.7,
                                    1.0:16.1
                            },
                            100:{
                                    0.25: 8.3,
                                    0.5: 11.9,
                                    10.75: 6.1,
                                    1.0:21.4
                            },
                            150:{
                                    0.25: 10.9,
                                    0.5: 17.3,
                                    20.75: 4.1,
                                    1.0:32.1
                            },
                            200:{
                                    0.25: 14.1,
                                    0.5: 22.9,
                                    30.75: 2.7,
                                    1.0:42.8
                            },
                            250:{
                                    0.25: 17.4,
                                    0.5: 28.6,
                                    40.75: 0.8,
                                    1.0:53.5
                            },
                            350:{
                                    0.25: 23.7,
                                    0.5: 39.3,
                                    50.75: 6.0,
                                    1.0:74.9
                            },
                            500:{
                                    0.25: 33.3,
                                    0.5: 55.6,
                                    70.75: 9.6,
                                    1.0:107.0
                            }
    }

    closest_gen_size = min(consumption_by_size.keys(), key=lambda x:abs(x-gen_size))
    closest_gen_load = min(consumption_by_size[closest_gen_size].keys(), key=lambda x:abs(x-load))

    return consumption_by_size[closest_gen_size][closest_gen_load]

def resample_power_quality(data, frequency): # resample django query set using time

    resample_frequency = frequencies[frequency]

    if data.exists():
        data = data.values('post_datetime', 'voltage_l1_l12', 'voltage_l2_l23', 'voltage_l3_l31', 'current_l1', 'current_l2', 'current_l3', 'kw_l1', 'kw_l2', 'kw_l3', 'kvar_l1', 'kvar_l2', 'kvar_l3', 'power_factor_l1', 'power_factor_l2', 'power_factor_l3', 'total_kw', 'total_pf', 'avg_frequency', 'neutral_current', 'kwh_import')
        
        df = pd.DataFrame(data)
        # df["post_datetime"] = pd.to_datetime(df["post_datetime"])

        if frequencies[frequency] == "W": 
          
          resampled_data = df.resample(resample_frequency, label='right', on='post_datetime').mean().fillna(0)

        else:

          resampled_data= df.resample(resample_frequency, on='post_datetime').mean().fillna(0).round(2)
        
        number_of_rows = resampled_data.shape[0]

        result = {
                    "dates": {
                        "dates": resampled_data.index,
                        "units": ""
                    },
                    "voltage": {
                        "l1": resampled_data.voltage_l1_l12,
                        "l2": resampled_data.voltage_l2_l23,
                        "l3": resampled_data.voltage_l3_l31,
                        "neutral": [0]*number_of_rows,
                        "units": "volts"
                    },
                    "current": {
                        "l1": resampled_data.current_l1,
                        "l2": resampled_data.current_l2,
                        "l3": resampled_data.current_l3,
                        "neutral": [0]*number_of_rows,
                        "units": "amps"
                    },
                    "active_power": {
                        "l1": resampled_data.kw_l1,
                        "l2": resampled_data.kw_l2,
                        "l3": resampled_data.kw_l3,
                        "neutral": [0]*number_of_rows,
                        "units": "kW"
                    },
                    "reactive_power": {
                        "l1": resampled_data.kvar_l1,
                        "l2": resampled_data.kvar_l2,
                        "l3": resampled_data.kvar_l3,
                        "neutral": [0]*number_of_rows,
                        "units": "kVar"
                    },
                    "frequency": {
                        "average": resampled_data.avg_frequency,
                        "units": "hz"
                    },
                    "power_factor": {
                        "l1_l2_l3": resampled_data.total_pf,
                        "units": ""
                    },
                    "power_factor123": {
                        "l1": resampled_data.power_factor_l1,
                        "l2": resampled_data.power_factor_l2,
                        "l3": resampled_data.power_factor_l3,
                        "units": ""
                    }
        }

        return result
    else:

        result = {
                    "dates": {
                        "dates": [],
                        "units": ""
                    },
                    "voltage": {
                        "l1": [],
                        "l2": [],
                        "l3": [],
                        "neutral": [],
                        "units": "volts"
                    },
                    "current": {
                        "l1": [],
                        "l2": [],
                        "l3": [],
                        "neutral": [],
                        "units": "amps"
                    },
                    "active_power": {
                        "l1": [],
                        "l2": [],
                        "l3": [],
                        "neutral": [],
                        "units": "kW"
                    },
                    "reactive_power": {
                        "l1": [],
                        "l2": [],
                        "l3": [],
                        "neutral": [],
                        "units": "kVar"
                    },
                    "frequency": {
                        "average": [],
                        "units": "hz"
                    },
                    "power_factor": {
                        "l1_l2_l3": [],
                        "l1": [],
                        "l2": [],
                        "l3": [],
                        "units": ""
                    }
        }

        return result

def resample_power_demand(data, frequency): # resample django query set using time

    resample_frequency = frequencies[frequency]

    if data.exists():
        data = data.values('post_datetime','total_kw')
        
        df = pd.DataFrame(data)
        # df["post_datetime"] = pd.to_datetime(df["post_datetime"])

        if frequencies[frequency] == "W": 
          
          resampled_data = df.resample(resample_frequency, label='right', on='post_datetime').mean().fillna(0)

        else:
          resampled_data = df.resample(resample_frequency, on='post_datetime').agg(['min','max', 'mean']).fillna(0).round(2)
        
        number_of_rows = resampled_data.shape[0]

        result = {
                "dates": {
                "dates": resampled_data.index,
                "units": ""
              },
              "power_demand_values": {
                "demand": resampled_data.total_kw["mean"],
                "min": resampled_data.total_kw["min"],
                "max": resampled_data.total_kw["max"],
                "avg": resampled_data.total_kw["mean"],
                "units": "kW"
              }
        }

        return result

    else:
        result = {
                "dates": {
                "dates": [],
                "units": ""
              },
              "power_demand_values": {
                "demand": [0],
                "min": [],
                "max": [],
                "avg": [],
                "units": "kW"
              }
        }


        return result

def get_kwh_usage_periodically(dataframe, return_key = "diff", frequency = "15mins")->pd.DataFrame:
  """ TAKES PANDAS DATA FRAME OF KWH DATA AND RESAMPLES IT INTO  PERIODICAL PORTIONS BASED ON GIVEN FREQUENCY """

  resample_frequency = frequencies[frequency]

  dataframe.index = dataframe.post_datetime
  resampled = dataframe.resample(resample_frequency, on = "post_datetime", label='left').agg(['min'])

  max_values = dataframe.resample(resample_frequency, on = "post_datetime", label='left').agg(['max'])
  last_reading = max_values[('summary_energy_register_1', 'max')].iloc[-1] # get the max values of the range.

  original = resampled["summary_energy_register_1"].iloc[:]["min"] # GET MINS PER GROUP
  shifted = list(resampled["summary_energy_register_1"].iloc[1:]["min"]) # GET MINS PER GROUP SHIFTED TO THE RIGHT THIS IS BECAUSE CALCULATIONS ARE DONE USING THE MINIMUM FROM ONE DAY MINUS THE MINIMUM FROM ANOTHER DAY I.E FIRST READING OF DAY 2 - FIRST READING OF DAY 1

  shifted.append(last_reading) # add the last value ofthe maxes to the shifted range, this is to act as the absolute max or final reading which denotes the value of the current period i.e if today is friday 23 that last period is the consumption for the 23rd this fixes the issue where you couldn't see the current consumption.

  data = pd.DataFrame({"dates":original.index, "original":list(original), "shifted":list(shifted)})
  data[return_key]= data.shifted - data.original
  data.index = data.dates

  return data[[return_key]]

def get_last_readings(device):

    raw_data = json.loads(device.last_reading)

    try:
        data = raw_data["Data"][0]['Data']
        record_time = raw_data["Data"][0]["RecordTime"]

    except (KeyError, TypeError): # INCASE REMOTE REQUEST FAILS TO FETCH USE THIS DEFAULTS
        record_time = "1900-01-01T00:00:00.00000"
        data = []

    template = {
              "date": record_time,
              "data": {
                "phase_measures": [
                  {
                    "name": "voltage",
                    "l1": get_parameter_from_last_read("Voltage L1/L12", data),
                    "l2": get_parameter_from_last_read("Voltage L2/L23", data),
                    "l3": get_parameter_from_last_read("Voltage L3/L31", data),
                    "unit": "volts"
                  },
                  {
                    "name": "current",
                    "l1": get_parameter_from_last_read("Current L1", data),
                    "l2": get_parameter_from_last_read("Current L2", data),
                    "l3": get_parameter_from_last_read("Current L3", data),
                    "unit": "amps"
                  },
                  {
                    "name": "active_power",
                    "l1": get_parameter_from_last_read("kW L1", data),
                    "l2": get_parameter_from_last_read("kW L2", data),
                    "l3": get_parameter_from_last_read("kW L3", data),
                    "unit": "kW"
                  },
                  {
                    "name": "reactive_power",
                    "l1": get_parameter_from_last_read("kvar L1", data),
                    "l2": get_parameter_from_last_read("kvar L2", data),
                    "l3": get_parameter_from_last_read("kvar L3", data),
                    "unit": "kVAR"
                  },
                  {
                    "name": "apparent_power",
                    "l1": get_parameter_from_last_read("kva L1", data),
                    "l2": get_parameter_from_last_read("kva L2", data),
                    "l3": get_parameter_from_last_read("kva L3", data),
                    "unit": "kVA"
                  },
                  {
                    "name": "pf",
                    "l1": get_parameter_from_last_read("Power factor L1", data),
                    "l2": get_parameter_from_last_read("Power factor L2", data),
                    "l3": get_parameter_from_last_read("Power factor L3", data),
                    "unit": "pf"
                  }
                ],
                "totals": [
                  {
                    "name": "active_power",
                    "value": get_parameter_from_last_read("Total kW", data),
                    "unit": "kW"
                  },
                  {
                    "name": "reactive_power",
                    "value": get_parameter_from_last_read("Total kvar", data),
                    "unit": "kVAR"
                  },
                  {
                    "name": "apparent_power",
                    "value": get_parameter_from_last_read("Avg Frequency", data),
                    "unit": "kVA"
                  },
                  {
                    "name": "frequency",
                    "value": get_parameter_from_last_read("Power factor L3", data),
                    "unit": "hz"
                  },
                  {
                    "name": "pf",
                    "value": get_parameter_from_last_read("PF", data),
                    "unit": "pf"
                  },
                  {
                    "name": "Neutral current",
                    "value": get_parameter_from_last_read("Neutral current", data),
                    "unit": "A"
                  }
                ],
                "harmonic_distortion": [
                  {
                    "name": "voltage_thd_ln",
                    "l1": get_parameter_from_last_read("voltage_thd_l1", data),
                    "l2": get_parameter_from_last_read("voltage_thd_l2", data),
                    "l3": get_parameter_from_last_read("voltage_thd_l3", data),
                    "unit": "%"
                  },
                  {
                    "name": "current_thd",
                    "l1": get_parameter_from_last_read("current_thd_l1", data),
                    "l2": get_parameter_from_last_read("current_thd_l2", data),
                    "l3": get_parameter_from_last_read("current_thd_l3", data),
                    "unit": "%"
                  },
                  {
                    "name": "current_tdd",
                    "l1": get_parameter_from_last_read("current_tdd_l1", data),
                    "l2": get_parameter_from_last_read("current_tdd_l2", data),
                    "l3": get_parameter_from_last_read("current_tdd_l3", data),
                    "unit": "%"
                  }
                ],
                "energy": [
                  {
                    "name": "active_energy",
                    "value": get_parameter_from_last_read("kWh import", data),
                    "unit": "kWh"
                  },
                  {
                    "name": "active_energy_export",
                    "value": get_parameter_from_last_read("kWh export", data),
                    "unit": "kWh"
                  },
                  {
                    "name": "reactive_energy",
                    "value": get_parameter_from_last_read("kVAr total", data),
                    "unit": "kvarh"
                  },
                  {
                    "name": "apparent_energy",
                    "value": get_parameter_from_last_read("kVAh total", data),
                    "unit": "kvah"
                  }
                ],
                "demands": [
                  {
                    "name": "max_amp",
                    "l1": get_parameter_from_last_read("Max Amp. Demand L1", data),
                    "l2": get_parameter_from_last_read("Max Amp. Demand L2", data),
                    "l3": get_parameter_from_last_read("Max Amp. Demand L3", data),
                    "unit": "A"
                  }
                ],
                "total_demands": [
                  {
                    "name": "max_power_demand",
                    "value": get_parameter_from_last_read("Max. sliding window kW Demand", data),
                    "unit": "A"
                  },
                  {
                    "name": "accumulated_power_demand",
                    "value": get_parameter_from_last_read("Accum. kW Demand", data),
                    "unit": "kW"
                  },
                  {
                    "name": "max_kva_demand",
                    "value": get_parameter_from_last_read("Max. sliding window kVA Demand", data),
                    "unit": "kVA"
                  },
                  {
                    "name": "kva_demand",
                    "value": get_parameter_from_last_read("Present sliding window kVA Demand", data),
                    "unit": "kVA"
                  },
                  {
                    "name": "power_demand",
                    "value": get_parameter_from_last_read("Present sliding window kW Demand", data),
                    "unit": "kW"
                  },
                  {
                    "name": "accumulated_kva_demand",
                    "value": get_parameter_from_last_read("Accum. kVA Demand", data),
                    "unit": "kVA"
                  },
                  {
                    "name": "pf_import_at_sliding_winow",
                    "value": 0,
                    "unit": "pf"
                  }
                ]
              }
            }
    
    return template

def get_parameter_from_last_read(parameter, readings):

    for entry in readings:
        if entry.get("Description", 0) == parameter:
            # print(True, parameter, entry.get("Description", 0), entry.get("Value", 0))
            return entry.get("Value", 0)
    else:
        return 0

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)

        file = open("temp.pdf", "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()

        return pdf

    @staticmethod
    def render_to_file(path: str, params: dict, receiver: object):

        template = get_template(path)
        html = template.render(params)
        file_name = "{0}-{1}.pdf".format(str(datetime.now()).replace(":", ""), random.randint(1, 1000000))
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "media", "pdfs", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)

        return dict(file_name = file_name, 
                    file_path = file_path)