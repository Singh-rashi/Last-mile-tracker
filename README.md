# Last-Mile Delivery Tracker

This is my submission for the Daffodil 1st round project. I have built a functional delivery tracking system using Python and Flask that handles order pricing, zones, and agent assignments.


---

###  Features I implemented:

1. **Weight & Rate Calculation:**
   - The system calculates **Volumetric Weight** using `(Length * Width * Height) / 5000`.
   - It automatically compares this to the **Actual Weight** and uses the higher value for billing.
   - I added a COD surcharge for Cash on Delivery orders.

2. **Zone Detection:**
   - I mapped pincodes to specific zones. 
   - The app detects if an order is "Intra-zone" (same zone) or "Inter-zone" (different zones) to apply the correct pricing.

3. **Auto-Assignment:**
   - When a new order is placed, the system automatically finds a delivery agent who belongs to the pickup zone and assigns the order to them.

4. **Tracking History:**
   - Instead of just updating a status, I created a separate table for History. Every time a status changes, a new record is added. This ensures a permanent audit trail that cannot be changed.

---

###  Tech Stack
- **Language:** Python 3.12
- **Framework:** Flask
- **Database:** SQLite (SQLAlchemy)


---

###  How to run it on your machine:

1. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
