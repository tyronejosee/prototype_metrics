from datetime import datetime
import random
import time

import numpy as np
import requests


class MetricGenerator:
    def __init__(self, pushgateway_url="http://localhost:9091") -> None:
        self.pushgateway_url = pushgateway_url
        self.running = True

        # Initialize metric states for realistic simulation
        self.cpu_base = 20.0  # Base CPU usage
        self.memory_base = 30.0  # Base memory usage
        self.request_count = 0
        self.error_count = 0

    def generate_cpu_usage(self) -> float:
        """Generate realistic CPU usage with some variability and spikes"""
        # Random walk with occasional spikes
        spike = random.random() < 0.1  # 10% chance of spike
        if spike:
            usage = min(95, self.cpu_base + random.uniform(30, 50))
        else:
            # Normal variation
            change = random.uniform(-5, 5)
            self.cpu_base = max(5, min(80, self.cpu_base + change))
            usage = self.cpu_base + random.uniform(-3, 3)

        return max(0, min(100, usage))

    def generate_memory_usage(self) -> float:
        """Generate realistic memory usage"""
        # Memory tends to grow slowly and then reset
        if random.random() < 0.05:  # 5% chance of reset (garbage collection)
            self.memory_base = random.uniform(15, 25)
        else:
            growth = random.uniform(-1, 2)  # Slight growth tendency
            self.memory_base = max(10, min(85, self.memory_base + growth))

        return self.memory_base + random.uniform(-2, 2)

    def generate_request_metrics(self) -> tuple:
        """Generate request and error counts"""
        # Simulate varying request loads
        hour = datetime.now().hour
        base_requests = 10

        # Higher load during business hours
        if 9 <= hour <= 17:
            base_requests = 25
        elif 18 <= hour <= 22:
            base_requests = 15

        new_requests = np.random.poisson(base_requests)
        self.request_count += new_requests

        # Errors occur in about 2-5% of requests
        if new_requests > 0:
            error_rate = random.uniform(0.02, 0.05)
            new_errors = np.random.binomial(new_requests, error_rate)
            self.error_count += new_errors

        return self.request_count, self.error_count

    def send_metrics_to_pushgateway(self, metrics):
        """Send metrics to Prometheus Pushgateway"""
        job_name = "system_monitor"
        instance_name = "demo_app"

        # Format metrics for Pushgateway
        metric_text = ""
        for metric_name, value in metrics.items():
            metric_text += f"{metric_name} {value}\n"

        url = f"{self.pushgateway_url}/metrics/job/{job_name}/instance/{instance_name}"

        try:
            response = requests.post(
                url,
                data=metric_text,
                headers={"Content-Type": "text/plain; version=0.0.4"},
            )

            if response.status_code == 200:
                print(
                    f"✓ Metrics sent successfully at {datetime.now().strftime('%H:%M:%S')}"
                )
            else:
                print(f"✗ Failed to send metrics: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Error sending metrics: {e}")

    def run_continuous(self, interval=10) -> None:
        """Run metric generation continuously"""
        print("🚀 Starting metric generator...")
        print(f"📊 Sending metrics every {interval} seconds")
        print(f"🎯 Pushgateway URL: {self.pushgateway_url}")
        print("Press Ctrl+C to stop\n")

        try:
            while self.running:
                # Generate current metrics
                cpu_usage = self.generate_cpu_usage()
                memory_usage = self.generate_memory_usage()
                request_count, error_count = self.generate_request_metrics()

                metrics = {
                    "cpu_usage_percent": cpu_usage,
                    "memory_usage_percent": memory_usage,
                    "request_count_total": request_count,
                    "error_count_total": error_count,
                }

                # Send to Pushgateway
                self.send_metrics_to_pushgateway(metrics)

                # Print current values
                print(
                    f"CPU: {cpu_usage:.1f}% | Memory: {memory_usage:.1f}% | "
                    f"Requests: {request_count} | Errors: {error_count}"
                )

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n🛑 Stopping metric generator...")
            self.running = False


def main():
    """Main function to run the metric generator"""
    print("=" * 60)
    print("🔥 GRAFANA METRICS GENERATOR")
    print("=" * 60)

    # Wait for services to start up
    print("⏳ Waiting for services to start (30 seconds)...")
    time.sleep(30)

    generator = MetricGenerator()
    generator.run_continuous(interval=10)


if __name__ == "__main__":
    main()
