# Network Utilization Monitor using SDN

## Problem Statement
This project implements a Software Defined Networking (SDN) based Network Utilization Monitor using Mininet and the Ryu Controller. The controller periodically collects switch port statistics and calculates bandwidth utilization to monitor real-time network traffic in the topology.

---

## Objective
- Monitor traffic flowing through SDN switches
- Collect byte counters from switch ports
- Estimate bandwidth utilization periodically
- Display TX/RX utilization in Mbps
- Demonstrate controller-switch interaction using OpenFlow

---

## Tools Used
- Mininet
- Ryu Controller
- OpenFlow 1.3
- Ubuntu Virtual Machine
- iperf
- Wireshark (Optional)

---

## Topology Used

```text
h1 ---- s1 ---- s2 ---- h2
```

---

## Project Files

```text
SDN_Project/
├── topology.py
├── network_monitor.py
└── README.md
```

---

## Execution Steps

### 1. Start Ryu Controller

```bash
ryu-manager network_monitor.py
```

---

### 2. Start Mininet Topology

```bash
sudo mn --custom topology.py --topo monitor --controller remote --switch ovsk,protocols=OpenFlow13
```

---

### 3. Check Topology Connections

```bash
net
```

---

### 4. Test Connectivity

```bash
pingall
```

---

### 5. Generate Traffic

Start iperf server:

```bash
h2 iperf -s &
```

Start iperf client:

```bash
h1 iperf -c h2 -t 20
```

---

## Controller Logic
The Ryu controller:
- Handles PacketIn events
- Communicates with switches using OpenFlow 1.3
- Periodically requests port statistics every 2 seconds
- Calculates bandwidth utilization using byte counters
- Displays TX/RX Mbps in controller terminal

---

## Bandwidth Calculation

Bandwidth is calculated as:

```text
Bandwidth = (New Bytes - Old Bytes) / Time Interval
```

Converted to Mbps:

```text
Mbps = (Bandwidth × 8) / 10^6
```

---

## Validation Scenarios

### Scenario 1: No Traffic
When no traffic is generated:
- Utilization remains approximately 0 Mbps

### Scenario 2: High Traffic
When traffic is generated using iperf:
- Utilization increases significantly

---

## Flow Table Commands

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s2
```

---

## Wireshark Observation
OpenFlow packets observed include:
- HELLO
- FEATURES_REQUEST / REPLY
- PACKET_IN
- MULTIPART_REQUEST / REPLY

---

## Results
- Successfully established controller-switch communication
- Successfully monitored switch port statistics
- Real-time bandwidth utilization displayed
- Traffic generation verified through iperf
- OpenFlow communication verified through Wireshark

---

## Conclusion
The SDN-based Network Utilization Monitor successfully demonstrates controller-switch interaction, flow handling, and centralized network monitoring using Mininet and Ryu. The controller periodically polls switch statistics and computes bandwidth utilization in real time.

---

## Proof of Execution

### Controller Startup
<img width="975" height="151" alt="image" src="https://github.com/user-attachments/assets/aeb79cc4-1ea3-4488-b670-0c617539da77" />


### Mininet Topology Initialization
<img width="742" height="283" alt="image" src="https://github.com/user-attachments/assets/e3060c41-8789-41e0-9a46-14583c8a465b" />


### Pingall Output
<img width="645" height="165" alt="image" src="https://github.com/user-attachments/assets/57b731c3-023f-4dc5-90ec-15e009463bb7" />

### iperf Traffic Generation
<img width="975" height="221" alt="image" src="https://github.com/user-attachments/assets/9cb4ffe2-ac50-4b1c-99f2-aaddf0a30817" />

### No Traffic Utilization
<img width="975" height="332" alt="image" src="https://github.com/user-attachments/assets/220f3e99-a06e-44e6-8118-348747300622" />

### High Traffic Utilization
<img width="846" height="190" alt="image" src="https://github.com/user-attachments/assets/9d3f3303-450e-4aa5-8501-b4fa58a3ed8a" />

### Flow Table s1 and Flow Table s2
<img width="975" height="194" alt="image" src="https://github.com/user-attachments/assets/61aabf6f-ad21-418c-91cc-3ef5ee618031" />

### Closing the connection
<img width="546" height="346" alt="image" src="https://github.com/user-attachments/assets/e55005f8-c4bc-4048-a96d-534f3a1b2c89" />


---

## References
1. Mininet Documentation  
2. Ryu SDN Framework Documentation  
3. OpenFlow Specification  
4. Ubuntu/Linux Manual Pages
