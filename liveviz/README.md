## XMR Nonce Live Visualizer

A simple tool to let us visualize, analyze and investigate nonce-distribution anomalies in a waterfall like chart over block-height, with difficulty as additional marker line.

![Image](example.jpg?raw=true)

### Demo

https://apollo.open-resource.org/flight-control/noncewatch/

### Run locally

```
$ git clone https://github.com/noncesense-research-lab/nonce_distribution.git
$ cd nonce_distribution/liveviz
$ python2 -m SimpleHTTPServer 6767
```

Point browser towards http://localhost:6767/

### Convert data from CSV

In order to use the csv data, we need to convert it to json:

```
./convertjson.py nonce-input-data.csv > blockdata.json
```

Currently the converter expects the following CSV format,
as per @xiphon's definition in the last dump:

```
difficulty,height,nonce,timestamp
```

If there is a header line in the CSV it's best to strip it for the moment
until we have common ground for format/parser.

### Future

Idealy, there would be some time series database populated with past data and
constantly updated with new data and feeding json directly to this client instead
of the static json file like now.
