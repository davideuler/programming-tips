# How to Metric Data by Dropwizard Metrics

## Reference
https://www.baeldung.com/dropwizard-metrics

https://metrics.dropwizard.io/3.1.0/getting-started/




## Example to Show histogram of latency difference in Singapore and Toronto 

Example from:
https://blog.aawadia.dev/2022/06/01/rafting-toronto-singapore/

Maven dependency:
```
<dependency>
    <groupId>io.dropwizard.metrics</groupId>
    <artifactId>metrics-core</artifactId>
    <version>3.1.2</version>
</dependency>
```

Metric statistics implementation as the following code.

```
val histogram = MetricRegistry().histogram("raft")
val singaporeStats = File("singapore.raft")
val torontoStats = File("toronto.raft")
val singaporeJson = JsonObject(singaporeStats.readText())
val torontoJsonObject = JsonObject(torontoStats.readText())

torontoJsonObject.forEach {
  if (!singaporeJson.containsKey(it.key)) println("does not contain ${it.key}").also { return@forEach }

  val singaporeValue = singaporeJson.getString(it.key).toLong()
  val torontoValue = it.value.toString().toLong()
  histogram.update(abs(singaporeValue - torontoValue))
}

// snapshot contains the max, min, mean, median etc
val snapshot = histogram.snapshot
```

The stats were as follows

```
| max   | min  | mean  | median | 75th percentile | 95th Percentile | 99th Percentile | 99.9th percentile |
|-------|------|-------|--------|-----------------|-----------------|-----------------|-------------------|
| 288ms | 95ms | 162ms | 157ms  | 165ms           | 192ms           | 236ms           | 283ms             |


## Another report example

Reporter
When we need to output our measurements, we can use Reporter. This is an interface, and the metrics-core module provides several implementations of it, 
such as ConsoleReporter, CsvReporter, Slf4jReporter, JmxReporter and so on.

Here we use ConsoleReporter as an example:

```
MetricRegistry metricRegistry = new MetricRegistry();

Meter meter = metricRegistry.meter("meter");
meter.mark();
meter.mark(200);
Histogram histogram = metricRegistry.histogram("histogram");
histogram.update(12);
histogram.update(17);
Counter counter = metricRegistry.counter("counter");
counter.inc();
counter.dec();

ConsoleReporter reporter = ConsoleReporter.forRegistry(metricRegistry).build();
reporter.start(5, TimeUnit.MICROSECONDS);
reporter.report();
```
