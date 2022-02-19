import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
import matplotlib.dates as mdates
import os
from os.path import isfile, join

source_files = [f for f in os.listdir('raw_data') if isfile(join('raw_data', f))]

# Loop though source files
for house in source_files:

  # Prepare output folders
  out_folder = f'out_files/{house.replace(".csv", "")}'
  if not os.path.exists(out_folder):
    os.makedirs(out_folder)

  # Read data from the first csv file
  df = pd.read_csv(f'raw_data/{house}',index_col=0, parse_dates=True)
  df.index = df.index + datetime.timedelta(hours = 8)
  # print(df.head())

  # Extract power column
  power_data = df['Power']
  print(power_data.head())

  #Find the maximum power value and timestamp
  max_power = power_data.max()
  max_index = power_data.idxmax()
  print(max_index)

  # #String Formatting
  max_time = max_index.strftime("%H:%M")
  max_power_string = "Max Power: {:.2f} W at {}".format(max_power, max_time)
  print(max_power_string + '\n')

  # #Find the minimum power value and timestamp
  min_power = power_data.min()
  min_index = power_data.idxmin()

  # #String Formatting
  min_time = min_index.strftime("%H:%M")
  min_power_string = "Min Power: {:.2f} W at {}".format(min_power, min_time)
  print(min_power_string + '\n')

  #Energy in Joules: calculate integral dW = P*dt
  energy_joules = np.cumsum(power_data*120)
  # print(energy_joules)

  #Convert from joules to kWh
  energy_kwh = energy_joules/3600000
  # print(energy_kwh)

  #Find the total energy consumption for the 24-hour cycle
  total_kwh = energy_kwh.max()
  total_kwh_string = "Total Energy Consumption: {:.2f} kWh".format(total_kwh)
  print(total_kwh_string + '\n')

  #Calculate the total cost of the 24-hour cycle, assuming a rate of R1/kWh
  total_cost = "Total Cost (24 hour cycle): R{:.2f}".format(total_kwh)
  print(total_cost + '\n')

  # Append energy data back to the dataframe
  df['Energy'] = energy_kwh
  # print(df.head())

  #Plot Power data using pyplot (use plot_date!)
  plt.plot_date(df.index + datetime.timedelta(hours = 8),power_data,'-')

  #Plot Maximum and Minimum Value
  plt.plot_date(max_index + datetime.timedelta(hours = 8),max_power,'r.')
  plt.text(max_index + datetime.timedelta(hours = 8),max_power+15,max_power_string)
  plt.plot_date(min_index + datetime.timedelta(hours = 8),min_power,'r.')

  #Inspecting the dataframe, it can be seen that it has a frequency of 2 minutes. Set df.index.freq = '2T' where T is minutes
  df.index.freq = '2T'
  plt.text(min_index + datetime.timedelta(hours = 8) -150*df.index.freq,min_power-60,min_power_string)

  #Title and Axis Lables
  plt.title('House 0 Power Data')
  plt.ylabel('Power [W]')
  plt.xlabel('Date')

  #Format x-axis to only display hours and minutes
  plt.gcf().autofmt_xdate()
  myFmt = mdates.DateFormatter('%H:%M')
  plt.gca().xaxis.set_major_formatter(myFmt)

  #for replit use: plt.savefig('power_max_min.png')
  # plt.show()
  plt.savefig(f'{out_folder}/power_max_min.png')

  # Plot energy consumption
  df.plot(kind='line', y = 'Energy', color = 'r')
  plt.title('House 0 Energy Consumption')
  plt.ylabel('Energy [kWh]')

  #for replit use: plt.savefig('energy_consumption.png')
  # plt.show()
  plt.savefig(f'{out_folder}/energy_consumption.png')
  plt.clf()

  df.to_csv(f'{out_folder}/{house.replace(".csv", "_appended.csv")}')

