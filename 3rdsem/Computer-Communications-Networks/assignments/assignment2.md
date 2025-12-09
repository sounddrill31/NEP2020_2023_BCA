---
order: 2
title: Assignment 2
clanker: true
---
## Q1. Explain Checksum with example.
Checksum is an error detection method used by upper-layer protocols, considered more reliable than LRC, VRC, and CRC. It employs a Checksum Generator on the sender side and a Checksum Checker on the receiver side to create a unique number from the data for integrity verification. When data is created, a checksum is calculated and sent or saved with it. Upon accessing the data, the checksum is recalculated, and if the two match, the data is likely error-free.

- EXAMPLE:

    Sender Side:
    ```txt
    10101001        subunit 1  
    00111001        subunit 2        
    11100010        sum (using 1s complement)       
    00011101        checksum (complement of sum)
    ```

    Receiver Side:
    ```txt
    10101001        subunit 1  
    00111001        subunit 2     
    00011101        checksum 
    11111111        sum
    00000000        sum's complement
    ```
    Result is zero, it means no error. [[1](https://www.geeksforgeeks.org/error-detection-code-checksum/)]


## Q2. Explain CRC with example.
A cyclic redundancy check (CRC) is a mathematical technique that provides a way to detect errors in transmitted data by appending a special code, called a checksum, to the original information. CRC plays a vital role in identifying and correcting potential data corruption in networking, where reliable data transfer is paramount. [[1](https://www.purestorage.com/knowledge/cyclic-redundancy-check.html)]
- EXAMPLE: 
    
    Sender Side:
    ```txt
    Data word to be sent - 100100
    Key - 1101 [ Or generator polynomial x3 + x2 + 1]
    ```

    ![sender](https://media.geeksforgeeks.org/wp-content/uploads/rational1.jpg)

    Therefore, the remainder is 001 and hence the encoded data sent is 100100001.
    
    Receiver Side:
    ```txt
    Code word received at the receiver side  100100001
    ```

    ![receiver](https://media.geeksforgeeks.org/wp-content/uploads/rational2.jpg)

    Therefore, the remainder is all zeros. Hence, the
    data received has no error. [[2](https://www.geeksforgeeks.org/modulo-2-binary-division/)]


## Q3.Explain Hamming Code with a neat example.
Hamming code is an error-correcting method developed by Richard Hamming in the 1950s. It adds extra bits to data, enabling the detection and correction of single-bit errors during transmission or storage, thus improving the reliability of communication systems and digital storage. [[1](https://www.geeksforgeeks.org/hamming-code-in-computer-network/)]

<!-- TODO: Neat Example -->

## Q4.Explain Stop and Wait Protocol. 
The Stop-and-Wait protocol is a flow control mechanism used in the data link layer for transmitting data over noiseless channels. In this protocol, the sender transmits a frame and then waits for an acknowledgment from the receiver before sending the next frame. It allows unidirectional data transmission, meaning only one direction (sending or receiving) occurs at a time. While it effectively manages flow control, it does not include any error control mechanisms. [[1](https://www.javatpoint.com/stop-and-wait-protocol)]


## Q5.Explain Stop and Wait Automatic Repeat Request with a neat diagram.
The Stop and Wait ARQ protocol sends a data frame and then waits for an acknowledgment (ACK) from the receiver. The ACK indicates that the receiver successfully received the data frame. After receiving the ACK from the receiver, the sender delivers the next data frame. So there is a stop before the next data frame is transferred, hence it is known as the Stop and Wait ARQ protocol. [[1](https://www.geeksforgeeks.org/stop-and-wait-arq/)]

![SAWARQ](https://media.geeksforgeeks.org/wp-content/uploads/Stop-and-Wait-ARQ.png)


## Q6.Explain Go Back-N Automatic Repeat Request.
The Go-Back-N (GBN) protocol is a sliding window protocol used in networking for reliable data transmission. It is part of the Automatic Repeat reQuest (ARQ) protocols, which ensure that data is correctly received and that any lost or corrupted packets are retransmitted. [[1](https://www.geeksforgeeks.org/sliding-window-protocol-set-2-receiver-side/)]


## Q7.Explain Selective Repeat Request.
Selective Repeat Request (SRR) is an error control protocol used in data communication to ensure reliable transmission of data frames. It is part of the Automatic Repeat reQuest (ARQ) family of protocols and is particularly effective in managing the retransmission of lost or corrupted frames without requiring the retransmission of all previously sent frames. [[1](https://www.geeksforgeeks.org/sliding-window-protocol-set-3-selective-repeat/)]


## Q8.Explain Designing Issues with a Network Layer.
1. **Reliability**:
    - Reliability is a key design issue, as network components may be unreliable, leading to data loss. Effective error detection and correction mechanisms are essential for maintaining data integrity.
2. **Addressing**:
    - Addressing is fundamental in network design for identifying senders and receivers. Proper management of addresses facilitates efficient communication and ensures data reaches its intended destination.
- **Error Control**:
    - Error control is vital due to imperfections in communication circuits. Design must include error-detecting and correcting codes agreed upon by both sender and receiver to protect data integrity.
- **Flow Control**:
    - Flow control is crucial for balancing data transmission between senders and receivers to prevent data loss. Design mechanisms like buffer adjustments or message segmentation manage speed mismatches. [[1](https://www.javatpoint.com/design-issues-for-the-layers-of-computer-networks)]


## Q9.Explain Distance Vector Routing Algorithm.
Distance Vector Routing is an algorithm where a router calculates distances to destinations based solely on its immediate neighbors. It shares its routing table with directly connected routers at regular intervals, allowing them to update their tables. The Bellman-Ford algorithm is typically used for route computation. Despite its simplicity, Distance Vector Routing faces issues like the Count to Infinity problem and persistent routing loops. [[1](https://www.geeksforgeeks.org/difference-between-distance-vector-routing-and-link-state-routing/)]


## Q10.Explain Link Status Routing Algorithm.
The Link Status Routing Algorithm, or Link State Routing, is a dynamic routing protocol where each router maintains a complete view of the entire network. Unlike Distance Vector protocols, routers flood their link state information across the network to ensure all routers share the same topology. Dijkstra’s Algorithm is used to compute the shortest paths to all destinations, preventing persistent routing loops. However, this flooding can lead to increased network traffic. [[1](https://www.geeksforgeeks.org/difference-between-distance-vector-routing-and-link-state-routing/)]


## Q11.Explain Leaky Bucket Algorithm with an neat diagram.
A simple leaky bucket algorithm can be implemented using FIFO queue. A FIFO queue holds the packets. If the traffic consists of fixed-size packets (e.g., cells in ATM networks), the process removes a fixed number of packets from the queue at each tick of the clock. If the traffic consists of variable-length packets, the fixed output rate must be based on the number of bytes or bits. 

![leakyb](https://media.geeksforgeeks.org/wp-content/uploads/leakyTap-1.png)


## Q12.Explain Token Bucket Algorithm with an neat diagram.
The Token Bucket algorithm is used in networking for traffic shaping and rate limiting. It controls the amount of data sent or received within a period, ensuring traffic conforms to a specified rate. It helps differentiate performance based on network requirements and provides predictable or guaranteed performance. 

![tokenb](https://media.geeksforgeeks.org/wp-content/uploads/20240116162804/Blank-diagram-(7).png)


## Q13.Explain service provided by Transport Layer Protocol.
- **Process to Process Delivery**: 
    - The Transport Layer uses port numbers (16-bit addresses) to deliver data segments to the correct process on a host, differentiating multiple processes running simultaneously.
- **End-to-End Connection between Hosts**:
    - It establishes connections using protocols like TCP (reliable, connection-oriented) and UDP (unreliable, best-effort delivery), suitable for different applications such as video conferencing.
- **Multiplexing and Demultiplexing**: 
    - Multiplexing combines data from multiple processes into a single packet using port numbers, while demultiplexing distributes incoming packets to the appropriate processes on the receiver's side.
- **Data Integrity and Error Correction**: 
    - It ensures data integrity by using error detection codes and checksums, along with ACK/NACK services to confirm the successful delivery of data.
- **Flow Control**: 
    - Flow control prevents data loss by managing the rate of data transmission between sender and receiver, primarily using the sliding window protocol to adjust the flow based on receiver capacity. [[1](https://www.geeksforgeeks.org/transport-layer-responsibilities/)]


## Q14.Explain the elements of Transport Layer.
Transport Layer is a 4th layer from the top. The main role of the transport layer is to provide the communication services directly to the application processes running on different hosts. The elements of Transport Layer are: 
- **Error Control**:  
    - The Data Link Layer checks for errors only between devices on the same link, so errors introduced by routers are not detected. In contrast, the Transport Layer performs end-to-end error checking to ensure that packets arrive correctly.
- **Sequence Control**:  
    - On the sending end, the Transport Layer ensures that packets from upper layers are suitable for lower layers, while on the receiving end, it guarantees the correct reassembly of the transmission's segments.
- **Loss Control**:  
    - The Transport Layer ensures that all fragments of a transmission arrive at the destination. On the sending end, it assigns sequence numbers to each fragment, enabling the receiver's Transport Layer to identify any missing segments.
- **Flow Control**:  

    - Flow control prevents the sender from overwhelming the receiver, which can lead to packet loss and increased network congestion. The Transport Layer employs the sliding window protocol to efficiently manage data transmission and ensure the receiver is not overloaded. This protocol operates on a byte-oriented basis rather than a frame-oriented one. [[1](https://www.javatpoint.com/computer-network-transport-layer)]
 
use-AI-here-please: "Please elaborate on the problems that come with flow control"

