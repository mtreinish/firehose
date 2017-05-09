import csv
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas

# Dedupe data
data = {}
data_pub = {}
with open('stresstest.dat', 'r') as fd:
    csv_file = csv.reader(fd, delimiter=':')
    for row in csv_file:
        if row[4] == 'Subscriber Avg. Throughput':
            continue
        if row[0] not in data:
            data[row[0]] = {row[1]: [float(row[4])]}
            data_pub[row[0]] = {row[1]: [float(row[8])]}
        elif row[1] not in data[row[0]]:
            data[row[0]][row[1]] = [float(row[4])]
            data_pub[row[0]][row[1]] = [float(row[8])]
        elif row[1] in data[row[0]]:
            data[row[0]][row[1]].append(float(row[4]))
            data_pub[row[0]][row[1]].append(float(row[8]))

with open('stresstest-prune.dat', 'w') as fd:
    csv_out = csv.writer(fd, delimiter=':')
    csv_out.writerow(['Subscriber Count', 'Publisher Count',
                      'Subscriber Avg. Throughput'])
    for sub_count in data:
        for pub_count in data[sub_count]:
            if len(data[sub_count][pub_count]) > 5:
                arr = np.array(data[sub_count][pub_count])
                res = np.mean(arr)
                csv_out.writerow([sub_count, pub_count, res])

with open('stresstest-pub-prune.dat', 'w') as fd:
    csv_out = csv.writer(fd, delimiter=':')
    csv_out.writerow(['Subscriber Count', 'Publisher Count',
                      'Publisher Avg. Throughput'])
    for sub_count in data_pub:
        for pub_count in data_pub[sub_count]:
            if len(data_pub[sub_count][pub_count]) > 5:
                arr = np.array(data_pub[sub_count][pub_count])
                res = np.mean(arr)
                csv_out.writerow([sub_count, pub_count, res])


bench_dat = pandas.read_csv('stresstest-prune.dat', ':')
bench_pub_dat = pandas.read_csv('stresstest-pub-prune.dat', ':')

bench_prune = bench_dat.groupby(
    [
        'Subscriber Count',
        'Publisher Count'
    ])
out_bench = bench_prune.aggregate(np.mean)

fig = plt.figure()
ax = Axes3D(fig)
out_bench.reset_index(inplace=True)
print bench_dat

import matplotlib.ticker as mticker

def log_tick_formatter(val, pos=None):
    return "{:.2e}".format(2**val)

surf = ax.plot_trisurf(np.log2(bench_dat['Subscriber Count']),
                       np.log2(bench_dat['Publisher Count']),
                       bench_dat['Subscriber Avg. Throughput'],
                       cmap=cm.inferno,
                       linewidth=0.2)

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.xlabel('Number of Subscribers')
plt.ylabel('Number of Publishers')
plt.title('Subscriber Average Throughput (msg/sec)')
plt.savefig('sub_throughput.png', dpi=900)

fig = plt.figure()
ax = Axes3D(fig)
surf = ax.plot_trisurf(np.log2(bench_pub_dat['Publisher Count']),
                       np.log2(bench_pub_dat['Subscriber Count']),
                       bench_pub_dat['Publisher Avg. Throughput'],
                       cmap=cm.inferno,
                       linewidth=0.2)

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.ylabel('Number of Subscribers')
plt.xlabel('Number of Publishers')
plt.title('Publisher Average Throughput (msg/sec)')
plt.savefig('pub_throughput.png', dpi=900)
