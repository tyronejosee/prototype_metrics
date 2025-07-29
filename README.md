# Prototype Metrics

Complete Grafana + Prometheus monitoring setup with Docker Compose, designed for learning and experimentation.

![Main](image.jpg)

## 🏗️ Architecture Overview

- **Grafana**: Web interface for creating dashboards and visualizing metrics
- **Prometheus**: Time-series database that stores metrics
- **Pushgateway**: Allows batch jobs to push metrics to Prometheus
- **Python Script**: Generates realistic system metrics

## 🚀 Quick Start Guide

Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ (for the metric generator script)

Start the Services

```bash
# Start all services in the background
docker-compose up -d

# Check if all services are running
docker-compose ps
```

Install Python Dependencies

```bash
pip install -r requirements.txt
```

Run the Metric Generator

```bash
python metric_generator.py
```

Access the Services

- **Grafana**: <http://localhost:3000>
  - Username: `admin`
  - Password: `admin123`
  
- **Prometheus**: <http://localhost:9090>
- **Pushgateway**: <http://localhost:9091>

## 📊 Pre-configured Dashboard

The setup includes a pre-configured dashboard called "System Metrics Dashboard" that displays:

- CPU Usage
- Memory Usage  
- Request Count
- Error Count

## 🛠️ Customization Ideas

Adding New Metrics

1. Modify `metric_generator.py` to include new metrics
2. Update the dashboard JSON or create new panels in Grafana UI

Different Data Sources

- Replace Prometheus with InfluxDB for different time-series storage
- Add Loki for log aggregation
- Include Node Exporter for real system metrics

Advanced Features

- Set up alerting rules in Prometheus
- Add notification channels in Grafana
- Create custom alert conditions

## 🧪 Testing and Development

View Raw Metrics

Visit <http://localhost:9091/metrics> to see raw metrics from Pushgateway

Query Metrics in Prometheus

Go to <http://localhost:9090> and try these queries:

- `cpu_usage_percent`
- `memory_usage_percent`
- `rate(request_count_total[5m])`

Stop Everything

```bash
docker-compose down

# Remove volumes (caution: this deletes all data)
docker-compose down -v
```

## 📁 File Structure

```bash
prototype_grafana_prometheus/
├── docker-compose.yml          # Main orchestration file
├── prometheus/
│   └── prometheus.yml          # Prometheus configuration
├── datasources/
│   └── prometheus.yml          # Grafana datasource config
├── dashboards/
│   ├── dashboard.yml           # Dashboard provider config
│   └── system-metrics.json     # Pre-built dashboard
├── metric_generator.py         # Metric generation script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Troubleshooting

Services won't start

- Check Docker is running: `docker ps`
- Check logs: `docker-compose logs [service-name]`

No data in Grafana

- Verify Prometheus is scraping: <http://localhost:9090/targets>
- Check if metrics are being pushed: <http://localhost:9091/metrics>
- Ensure the Python script is running without errors

Can't access Grafana

- Wait a few minutes for services to fully start
- Check if port 3000 is available: `netstat -an | grep 3000`

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

Enjoy! 🎉
