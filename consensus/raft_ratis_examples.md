
**Raft course videos, and implementations**
https://raft.github.io/#implementations

**jraft user guide**
https://www.sofastack.tech/projects/sofa-jraft/jraft-user-guide/

**Raft Papers**

https://ramcloud.atlassian.net/wiki/download/attachments/6586375/raft.pdf

https://www.usenix.org/system/files/hotcloud19-paper-ahn.pdf

https://kudu.apache.org/docs/index.html#raft

https://home.apache.org/~szetszwo/presentations/20171115brown_bag.pdf

https://arxiv.org/pdf/1711.06964.pdf

https://github.com/maemual/raft-zh_cn

https://www.ballista.com/wp-content/uploads/2022/04/Rocks___Raft.pdf


**Ratis Example**

https://github.com/apache/iotdb

https://github.com/alpapad/raft-retry-log

https://github.com/tincopper/tomgs-java/

https://github.com/tincopper/tomgs-java/blob/2c92ea651e4a5c95a5632ea12f2f9d5094216919/learning-jraft/src/main/java/com/tomgs/ratis/customrpc/watchkv/core/RatisWatchKVServerStateMachine.java

https://github.com/alpapad/raft-retry-log/blob/0c4d5ee38d85bf22bbe4f2d852af0eaa0e10c066/retry-log-server/src/main/java/com/aktarma/retrylog/server/db/IDbBackend.java#L4


https://github.com/korandoru/zeronos/blob/main/zeronos-core/src/main/proto/Zeronos.proto
https://github.com/opendataio/ratis-shell

Ratis snapshot:
https://github.com/apache/ratis/blob/master/ratis-docs/src/site/markdown/snapshot.md

**Ozone & Alluxio**

https://blog.cloudera.com/apache-ozone-metadata-explained/

https://blog.cloudera.com/ozone-write-pipeline-v2-with-ratis-streaming/

https://github.com/Alluxio/alluxio

https://www.alluxio.io/blog/from-zookeeper-to-raft-how-alluxio-stores-file-system-state-with-high-availability-and-fault-tolerance/

https://www.youtube.com/watch?v=CSe7-6AYX5o&ab_channel=ApacheOzone-unofficial

OZone architecture:
https://blog.cloudera.com/apache-hadoop-ozone-object-store-architecture/
https://www.itweet.cn/2021/01/21/apache-ozone-object-store-architecture/

Ozone at Tencent:
https://mp.weixin.qq.com/s/6rtkmwjfI_Cl-hYMrDOOyA

Ozone docs:
https://docs.qq.com/doc/DZUJFSXFuZHFXRGZp


**Raft Election and Cluster Management**

The leader is selected through an elections
process that ensures only a candidate server with the most up-todate log can be elected as the leader.

Each server within a Raft cluster starts off as a follower with
a randomized timer. If the timer reaches zero before the server
receives a request from a leader, the server will kick of an election
by converting to a candidate and sending out a request for votes to
all the other servers in the cluster. Once a candidate receives a vote
from a majority of the nodes in the cluster, it converts to a leader
and starts sending heartbeat requests to all nodes in the cluster to
prevent another from starting a new election.

If the leader node for some reason subsequently goes down,
another server will start the election process once it’s randomized
timer runs down without having received any requests from the
leader. A new server can be added to an existing cluster at any
time and it will stay in a follower state once it starts receiving
heartbeat requests from the leader of the cluster. The leader of the
cluster receives the current index of the logs for all followers in
their response back to the heartbeat and therefore can replicate
data as needed to bring the servers up-to-date.

