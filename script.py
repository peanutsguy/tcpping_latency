import os
import subprocess
import socket
import csv
import time
from datetime import datetime, timezone

TCP_ENDPOINT = os.getenv("TCP_ENDPOINT")
TCP_PORT = int(os.getenv("TCP_PORT", "443"))
NUM_REQUESTS = int(os.getenv("NUM_REQUESTS", "10"))

def get_destination_ip(endpoint):
    try:
        hostname = endpoint.replace("https://", "").replace("http://", "").split("/")[0]
        return socket.gethostbyname(hostname)
    except Exception:
        return "unknown"

def run_tcpping(ip, port, count):
    results = []
    latencies = []
    for i in range(count):
        # print(i)
        start = time.time()
        try:
            proc = subprocess.run(
                ["./tcpping", "-x", "1", "-C", ip, str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            output = proc.stdout + proc.stderr
            # Parse latency from output (look for 'time=')
            latency = None
            error = ""
            for line in output.splitlines():
                if f"{ip} :" in line:
                    try:
                        value_str = line.split(":")[-1].strip()
                        if value_str == "-" or value_str == "255":
                            error = "timeout"
                            latency = None
                        else:
                            try:
                                value = float(value_str)
                                latency = round(value, 2)
                                latencies.append(latency)
                            except Exception:
                                error = "parse_error"
                                latency = None
                    except Exception:
                        error = "parse_error"
            results.append({
                "request": i + 1,
                "latency_ms": latency,
                "destination_ip": ip,
                "tcp_port": port,
                "msg": error
            })
        except Exception as e:
            results.append({
                "request": i + 1,
                "latency_ms": None,
                "destination_ip": ip,
                "tcp_port": port,
                "msg": str(e)
            })
        # time.sleep(1)
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else None
    return results, avg_latency

def save_results(results, avg_latency, start_timestamp, filename, destination_ip):
    keys = list(results[0].keys()) + ["start_time"]
    hostname = TCP_ENDPOINT.replace("https://", "").replace("http://", "").split("/")[0]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            r_copy = dict(r)
            r_copy["start_time"] = ""
            writer.writerow(r_copy)
        writer.writerow({**{k: "" for k in keys}, "request": "Average", "latency_ms": avg_latency, "start_time": start_timestamp, "msg": hostname})

if __name__ == "__main__":
    if not TCP_ENDPOINT:
        print("Please set TCP_ENDPOINT environment variable.")
        exit(1)
    start_timestamp = int(time.time())
    destination_ip = get_destination_ip(TCP_ENDPOINT)
    results, avg_latency = run_tcpping(destination_ip, TCP_PORT, NUM_REQUESTS)
    os.makedirs("results", exist_ok=True)
    filename = f"results/tcpping_results_{start_timestamp}.csv"
    save_results(results, avg_latency, start_timestamp, filename, destination_ip)
    print(f"Results saved to {filename}")
    print(f"Average TCP ping response time: {avg_latency:.2f} ms" if avg_latency is not None else "No successful responses to calculate average.")
    print(f"Execution time (UTC): {datetime.fromtimestamp(start_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
