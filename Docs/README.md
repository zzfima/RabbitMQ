# RabbitMQ + Grafana + Prometheus
### after finish this document you will be able run RabbitMQ producer, consumers and visualize it on Grafana web metrics UI
My OS windows 10, no dockers/kubernetes.

The metrics chain are: RabbitMQ -> rabbitmq_exporter -> Prometheus -> Grafana
Instead of RabbitMQ -> rabbitmq_exporter can be others, just configuration will be changed. Here all exporters: https://prometheus.io/docs/instrumenting/exporters/

•	Prometheus web panel: http://localhost:9090/
•	Grafana web panel: http://localhost:3000/
•	RabbitMQ web panel: http://localhost:15672/


### RabbitMQ
1. Download RabbitMQ from https://www.rabbitmq.com/download.html and install
2. After install go to C:\Users\yafimz\AppData\Roaming\RabbitMQ\ and create rabbitmq.conf
3. Inside put configuration:
```
listeners.tcp.default = 5673
```
This is address, listeners (rabbitmq_exporter) will bind to
4. Run it
5. Run some command to see it working: 
* rabbitmq-diagnostics -q status
6. go to http://localhost:15672, pass/username = guest, check it works

### Application producer consumer run
1. Download sources of this git and run (recieve.py can be run in multiple instances):
```
python send.py
python recieve.py
```

### rabbitmq_exporter
1. Download rabbitmq_exporter from  https://github.com/kbudde/rabbitmq_exporter
2. Add to downloaded source file config.example.json
3. Set next configuration in file :
```
{
    "rabbit_url": "http://127.0.0.1:15672",
    "rabbit_user": "guest",
    "rabbit_pass": "guest",
    "publish_port": "9419",
    "publish_addr": "",
    "output_format": "TTY",
    "ca_file": "ca.pem",
    "cert_file": "client-cert.pem",
    "key_file": "client-key.pem",
    "insecure_skip_verify": false,
    "exlude_metrics": [],
    "include_queues": ".*",
    "skip_queues": "^$",
    "skip_vhost": "^$",
    "include_vhost": ".*",
    "rabbit_capabilities": "no_sort,bert",
    "enabled_exporters": [
            "exchange",
            "node",
            "overview",
            "queue"
    ],
    "timeout": 30,
    "max_queues": 0
}
```
* Key configs:
  * "rabbit_url": "http://127.0.0.1:15672" this is address of RabbitMQ management
  * "rabbit_user": "guest" this is default RabbitMQ management user name
  * "rabbit_pass": "guest" this is default RabbitMQ management password
  * "publish_port": "9419" this port on localhost, where rabbitmq_exporter will send metrics
4. Run this file by next cmd:
```
rabbitmq_exporter -config-file config.example.json
```
5. It will use config.example.json configurations and run

### Prometheus
1. Download here: https://prometheus.io/download/ and install
2. In file prometheus-x.xx.x.windows-amd64\prometheus.yml change section scrape_configs:
```
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090']
    
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['localhost:9419']
    metrics_path: /metrics
    scheme: http
    basic_auth:
      username: guest
      password: guest
    tls_config:
      server_name: 'localhost'
      insecure_skip_verify: true
```
* Key configs:
  * targets: ['localhost:9090'] this is address of Prometheus web panel
  * targets: ['localhost:9419'] this is where from Prometheus get metrics (see previous section, there 9419 described)
3. Run it and open http://localhost:9090/service-discovery to see it up and RabbitMQ is up

### Grafana
1. Download from https://grafana.com/grafana/download?platform=windows and install it
2. Go to http://localhost:3000/ check it works
3. Download some dashboard, for example : https://grafana.com/grafana/dashboards/3662
