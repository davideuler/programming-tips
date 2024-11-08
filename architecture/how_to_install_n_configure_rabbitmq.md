
# RabbitMQ Howtos

由于阿里云上面的 RabbitMQ serveless 版本不支持 amq.rabbitmq.reply-to 消息，不能在 faststream 中使用。
手工搭建了 rabbitmq， 结合 faststream 来使用。

## Installation

<https://www.rabbitmq.com/docs/download>

Ubuntu 上面通过 Cloudsmith Mirror 来安装:

<https://www.rabbitmq.com/docs/install-debian#apt-quick-start-cloudsmith>


## Authentication and Access Control

<https://www.rabbitmq.com/docs/access-control>

rabbitmqctl change_password guest demo_pass

echo 'demo_password'| rabbitmqctl add_user 'david'

rabbitmqctl set_permissions -p "/" "david" ".*" ".*" ".*"

## Enable management plugin

<https://www.rabbitmq.com/docs/management>
<https://stackoverflow.com/questions/4545660/rabbitmq-creating-queues-and-bindings-from-command-line>

rabbitmq-plugins enable rabbitmq_management

可以从下面的地址下载 rabbitmqadmin 命令行工具：
http://node-hostname:15672/cli/

### Get the cli and make it available to use.
wget http://127.0.0.1:15672/cli/rabbitmqadmin
chmod +x rabbitmqadmin
mv rabbitmqadmin /etc/rabbitmq

#### 1.Add a user and permissions

rabbitmqctl add_user testuser testpassword
rabbitmqctl set_user_tags testuser administrator
rabbitmqctl set_permissions -p / testuser ".*" ".*" ".*"

#### 2.Make a virtual host and Set Permissions **

rabbitmqctl add_vhost Some_Virtual_Host
rabbitmqctl set_permissions -p Some_Virtual_Host guest ".*" ".*" ".*"

#### Make an Exchange

./rabbitmqadmin declare exchange --vhost=Some_Virtual_Host name=some_exchange type=direct

#### Make a Queue

./rabbitmqadmin declare queue --vhost=Some_Virtual_Host name=some_outgoing_queue durable=true

#### Make a Binding

./rabbitmqadmin --vhost="Some_Virtual_Host" declare binding source="some_exchange" destination_type="queue" destination="some_incoming_queue" routing_key="some_routing_key"


## Queue and exchange

<https://www.rabbitmq.com/docs/management-cli#declare-an-exchange>

Declare an exchange
rabbitmqadmin declare exchange --vhost="/" name=my-new-exchange type=fanout -u xxx -p xxxx

``` bash
./rabbitmqadmin declare exchange --vhost=/ name=test_exchange type=direct -u david -p password
```

* => exchange declared

Declare a queue, with optional parameters
rabbitmqadmin declare queue name=my-new-queue durable=false

* => queue declared

Publish a message

``` bash
rabbitmqadmin publish exchange=amq.default routing_key=test payload="hello, world"
```

* => Message published

And get it back
rabbitmqadmin get queue=test ackmode=ack_requeue_false

rabbitmqctl list_bindings -p my-vhost exchange_name queue_name
