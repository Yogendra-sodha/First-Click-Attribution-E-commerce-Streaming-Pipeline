👋 **Welcome to the First Click Attribution Stream Analytics Project!**

Stream processing is like a magical river where we handle lots of information flowing non-stop. Imagine it like a cool adventure with some important things to keep in mind. We want to figure out which click led to a purchase on e-commerce website. 🛒💻

📜 **Project Overview:**
I have used technologies like Apache Flink and Apache Kafka to create a real-time first click attribution pipeline. 

📝 **Project Objectives:**
1. Make checkout data super special by enriching with users and click data.
2. Find the first click a user made on a product within the last hour before making a purchase. This special click gets all the credit! 🏆
3. Keep track of all the checkouts and their special clicks in a table. 📊

🏰 **Project Architecture:**
Our project's magical river flow looks like this:
1. The website generates clicks and checkout data (like the source of the river).
2. These clicks and checkout data are sent to special topics in Apache Kafka, which acts like a transportation system for them (think of it as boats and rafts! 🚣).
3. Apache Flink comes in to read the data from Kafka topics and does some smart things with it (like wizards using magic spells! ✨).
4. We have a special place in our cluster (a big magical box!) to store the click data for the last hour only. We only remember one click per user for each product (like keeping only the important stuff).
5. Flink then adds user information to the checkout data by talking to the Postgres database.
6. The magic moment comes when Flink joins the enriched checkout data with the special clicks from the cluster state (like connecting puzzle pieces 🧩) to find the magical click that led to each checkout!
7. All the magical results are stored in a special table in the Postgres database (like keeping a record of our adventures).

🔧 **Code Design:**
We have some cool Python scripts that generate synthetic users, click and checkout data. We use Apache Table API to define how we want to process the data, like making our spells for enriching and attributing checkouts. We also define where we want to store the results (like making sure we keep track of everything!).

🔍 **Monitoring:**
We keep an eye on our adventure to make sure everything is smooth. We use Prometheus to collect metrics (like keeping track of our progress) and Graphana to visualize them (like having a magical dashboard).

🚀 Feel free to explore the code and have fun with streaming data like a wizard! 🧙‍♂️🌟
