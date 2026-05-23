# Monitoring Stack

Prometheus + Grafana metrics stack running on the Thinkcentre.

| Service | Description | URL |
|---|---|---|
| Grafana | Dashboards and visualization | https://grafana.apps.hematic.net |
| Prometheus | Metrics collection (internal) | http://192.168.1.126:9090 |
| cAdvisor | Thinkcentre container metrics | Internal |
| node-exporter | Thinkcentre system metrics | Internal |


## Scrape Targets

| Job | Target | Description |
|---|---|---|
| node-thinkcentre | node-exporter:9100 | Thinkcentre CPU/mem/disk/net |
| node-nuc | 192.168.1.7:9100 | NUC CPU/mem/disk/net |
| cadvisor | cadvisor:8080 | Docker container metrics |


## Environment Variables

| Variable | Description |
|---|---|
| `NETWORK` | Docker network (e.g. `proxy`) |
| `GRAFANA_USER` | Grafana admin username |
| `GRAFANA_PASSWORD` | Grafana admin password |

## Grafana Dashboard IDs

Import these in Grafana → Dashboards → Import:

| Dashboard | ID |
|---|---|
| Node Exporter Full | `1860` |
| Docker cAdvisor | `14282` |

## Deployment Notes

- Prometheus config is mounted from the git clone path — update `prometheus.yml` and redeploy to change scrape targets
- The NUC node_exporter is defined in `maintenance_stack/nuc/docker-compose.yml` with port 9100 exposed

## Updating

Redeploy via Komodo. Prometheus data and Grafana config are in named volumes and survive redeployment.
