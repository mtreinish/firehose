import matplotlib.pyplot as plt
import pandas

# Load Data
ram_usage = pandas.read_csv('manual_load_test_memory_usage.csv')
dates = ram_usage['Date']
del ram_usage['Date']
ram_usage =  ram_usage.set_index(pandas.to_datetime(dates))
cpu_usage = pandas.read_csv('manual_load_test_cpu_usage.csv')

cpu_dates = cpu_usage['Date']
del cpu_usage['Date']
cpu_usage = cpu_usage.set_index(pandas.to_datetime(cpu_dates))

print(ram_usage)
print(cpu_usage)

# Plot area usage
plt.figure()
ram_usage.plot.area(stacked=True)
plt.savefig('manual_load_ram_usage.png', dpi=900)

# Plot cpu usage
plt.figure()
cpu_usage.plot.area()
plt.savefig('manual_load_cpu_usage.png', dpi=900)
