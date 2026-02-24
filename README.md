# GeoStream: High-Performance Logistics & Routing Engine

**GeoStream** is an intelligent logistics engine designed to solve the "Last-Mile Delivery" challenge. Built for a Discrete Mathematics and Data Structures course, this project demonstrates how advanced algorithmic layers can optimize security, search, spatial indexing, and routing in a high-concurrency environment.

---

## System Architecture

GeoStream processes incoming requests through four distinct algorithmic layers to ensure maximum efficiency and scalability:

1.  **Security Layer (Bloom Filter):** Acts as a high-speed probabilistic gateway to intercept and block blacklisted User IDs in $O(k)$ time, preventing unauthorized access before hitting the main database.
    
2.  **Search Layer (Radix Tree):** A memory-efficient PATRICIA Trie that handles address and merchant name autocompletion. By compressing unbranched paths, it reduces memory overhead compared to standard Tries.
    

3.  **Spatial Layer (R-Tree):** Indexes thousands of driver GPS coordinates using Minimum Bounding Rectangles (MBRs). This allows for $O(\log n)$ proximity searches, pruning entire geographic regions from the search space instantly.
    

4.  **Optimization Layer (Fibonacci Heap):** Powers the priority queue for our routing engine. Leveraging $O(1)$ amortized insertion and `decrease-key` operations, it provides superior performance for real-time driver ranking and shortest-path calculations.
    

---

## Tech Stack & Implementation

* **Language:** Python 3.x
* **UI Framework:** Streamlit (Web Dashboard)
* **Mapping:** Folium (Geospatial Visualization)
* **Testing:** PyTest (Unit Testing Suite)
* **Environment:** GitHub Codespaces / Linux

