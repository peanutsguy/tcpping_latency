# Latency Test: TCP Ping Between Endpoints

[![Create and publish a Docker image](https://github.com/peanutsguy/tcpping_latency/actions/workflows/main.yaml/badge.svg)](https://github.com/peanutsguy/tcpping_latency/actions/workflows/main.yaml)

This project measures TCP round-trip latency from any Linux host to a specified endpoint using TCP ping.

## Features

- Measures TCP round-trip latency to a specified endpoint and port.
- Logs destination IP address for each request.
- Results saved in CSV format for analysis.
- Each run produces a uniquely named results file with the UNIX timestamp.
- The last row of the CSV contains the average response time and the start time UNIX timestamp.

## Requirements

- Python 3.8+
- traceroute
- Docker (optional)
- No external Python dependencies required for the TCP ping script.

## Usage

### 1. Direct Python Execution

#### Install dependencies (Alpine example):

```sh
apk add python3 traceroute
mkdir -p results
```

#### Download tcpping script and run:

```sh
wget https://raw.githubusercontent.com/deajan/tcpping/master/tcpping
chmod +x tcpping
export TCP_ENDPOINT="your-endpoint"
export TCP_PORT=443
export NUM_REQUESTS=10
python3 script.py
```

Results will be saved in the `results/` directory.

### 2. Using Docker

#### Build the Docker image:

```sh
docker build -f Dockerfile -t latency-tcp .
```

#### Or use the pre-built image from GitHub:

The container image is available at [`ghcr.io/peanutsguy/tcpping_latency`](https://github.com/peanutsguy/tcpping_latency).

#### Run the container:

```sh
docker run --rm \
  -e TCP_ENDPOINT="your-endpoint" \
  -e TCP_PORT=443 \
  -e NUM_REQUESTS=10 \
  -v $(pwd)/results:/app/results \
  ghcr.io/peanutsguy/tcpping_latency
```

Results will be available in your local `results/` directory.

## Output

CSV file columns:
- request
- latency_ms
- destination_ip
- tcp_port
- msg (error or status or hostname)
- start_time (only in the summary row)

The last row contains:
- request: "Average"
- latency_ms: average response time (ms)
- start_time: UNIX timestamp when the test started
- msg: hostname

## Security

- Do not commit sensitive credentials.
- Use environment variables for endpoint configuration.

## References

- [tcpping GitHub](https://github.com/deajan/tcpping)
