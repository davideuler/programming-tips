
# Raft from Toronto to Singapore

**[IT WORKS](https://blog.aawadia.dev/)** 

01-Jun-2022 

 [kotlin](https://blog.aawadia.dev/tags/kotlin/), [raft](https://blog.aawadia.dev/tags/raft/)

## Introduction

Raft has become the industry standard for replicating data across multiple nodes. The foundational concept is quite simple; if all nodes start from the same starting state S1 - and they all apply a sequence of operations in the same deterministic order then they will all end up at the same end state S2.

There is a leader node through which all the writes flow through - the follower nodes get the writes replicated to them only after the leader has achieved quorom - this means that there is a small gap of time between where the data exists on the leader node but hasn’t replicated to the follower nodes just yet. This gap is commonly called the ‘replication lag’

A concern comes up when apps have to replicate data across wide area networks [WAN] such as across data centers in multiple regions - think between US and Europe. Can raft still be used? Is the replication lag small enough? At the very minimum it takes a certain amount of time for the packets to move between continents - you cannot beat physics - can’t go faster than the speed of light.

## Experiment

To test out the replication lag between large geographical areas, I recently ran an experiment with two nodes replicating an in memory hash map via raft. The first server was located in Toronto and the second one was in Singapore - roughly 15,000 KM distance. I am using DigitalOcean as my cloud provider and these were the servers that I think are the furthest apart. In hindsight, Vultr might have had other data center locations that would have been even further but diminishing returns after a certain point.

Then I wrote 10,000 keys to the cluster with each node using the epoch as the value of when it applied the transaction.

After that, I calculated the difference between the values on the two nodes for each key and calculated some basic distribution statistics to get a feel of the replication lag.

## Raft

I used Apache’s Ratis library as my raft library. These were the dependencies added to the pom file

```
<dependency>
    <groupId>org.apache.ratis</groupId>
    <artifactId>ratis-server</artifactId>
    <version>2.3.0</version>
</dependency>
<dependency>
    <groupId>org.apache.ratis</groupId>
    <artifactId>ratis</artifactId>
    <version>2.3.0</version>
  <type>pom</type>
</dependency>
<dependency>
    <groupId>org.apache.ratis</groupId>
    <artifactId>ratis-grpc</artifactId>
    <version>2.3.0</version>
</dependency>
```

## Server code

```
// bring peers [ip:port of all the nodes in the cluster] in this list from some service discovery mechanism
val listOfPeers = mutableListOf<RaftPeer>()
peers.map { RaftPeer.newBuilder().setId($id).setAddress($ip).build() }.forEach { listOfPeers.add(it) }
val raftGroup = RaftGroup.valueOf(RaftGroupId.valueOf(UUID.fromString($uuid)), listOfPeers)

val port = NetUtils.createSocketAddr(me.address).port
GrpcConfigKeys.Server.setPort(properties, port);

val dataset = ConcurrentSkipListMap<String, String>()
val stateMachine = StateMachine(dataset)
val server = RaftServer.newBuilder()
    .setGroup(raftGroup)
    .setProperties(RaftProperties())
    .setServerId($my.id)
    .setStateMachine(stateMachine)
    .build()

// starts a grpc server
server.start()
```

## State machine

State machine is an interface that the app devs have to implement that wraps our data store, in this case it is an in memory hash map

```
class StateMachine(private val dataset: ConcurrentSkipListMap<String, String>) : BaseStateMachine() {
  // read
  override fun query(request: Message): CompletableFuture<Message> {
    return CompletableFuture.completedFuture(Message.valueOf(dataset?.get(request.content.toString(Charset.defaultCharset())) ?: "n/a"))
  }

  // write
  override fun applyTransaction(trx: TransactionContext): CompletableFuture<Message> {
    val entry = trx.logEntry
    updateLastAppliedTermIndex(entry.term, entry.index)
    val key = entry.stateMachineLogEntry.logData.toString(Charset.defaultCharset())
    // here the local epoch is used as the value on each node
    dataset[key] = System.currentTimeMillis().toString()
    return CompletableFuture.completedFuture(Message.valueOf(dataset[key]))
  }
}
```

## Client

The client makes the rpc request to issue the writes to the cluster

```
// same list of peers as the server code
val listOfPeers = mutableListOf<RaftPeer>()
peers.map { RaftPeer.newBuilder().setId($id).setAddress($ip).build() }.forEach { listOfPeers.add(it) }
val raftGroup = RaftGroup.valueOf(RaftGroupId.valueOf(UUID.fromString($uuid)), listOfPeers)
val raftClient = RaftClient.newBuilder()
    .setProperties(RaftProperties())
    .setRaftGroup(raftGroup)
    .setClientRpc(
      GrpcFactory(Parameters())
        .newRaftClientRpc(ClientId.randomId(), raftProperties)
    ).build()
// issue all these requests concurrently
repeat(10_000) {
    CoroutineScope(Dispatchers.IO).launch { raftClient.io().send(Message.valueOf("testme-${it}")) }
}
```

## Data collected

The hash map is then converted to json and collected from both nodes - the format of the data is

```
{
  "testme-0": "1654112670308",
  "testme-1": "1654112670435",
  "testme-10": "1654112670359",
  "testme-100": "1654112671405",
  "testme-1000": "1654112687565",
  "testme-1001": "1654112687573",
  "testme-1002": "1654112687670",
  "testme-1003": "1654112687715",
  "testme-1004": "1654112687727"
}
```

## Stats distribution

The json from both nodes were written out to two files and then parsed to get the stats

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
```

## Conclusion

The experiment shows that at most it took 0.3 seconds to have the same record on both servers and on average the record was available on both nodes in 162ms. This is more than fast enough for the vast majority of apps and WAN should not be used as an excuse to not use raft as the primary replication protocol. Both cockroachdb and yugabyte use raft when replicating cross regions as well.
