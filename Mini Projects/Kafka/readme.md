### Objective
In this tutorial, we will get our hands dirty and create our first streaming application backed by Apache Kafka using a Python client. We will try and make it as close as possible to a real-world Kafka application.


What we'll build is a real-time fraud detection system. We'll do so from scratch. We will
generate a stream of transactions and you will write a Python script to process those stream
of transactions to detect which ones are potential fraud.

### Steps
We first need to create a docker-compose.yml file, requirements.txt, and docker-compose.kafka.yml. The docker-compose.yml file will contain the contents of our generator and detector and our docker-compose.kafka.yml file will contain the details of our zookeeper/broker instance separately. The requirements file contains the contents required to install. Further steps noted below:

- Run command to spin up broker and zookeeper: docker-compose -f docker-compose.kafka.yml up --build (if the image needs to be rebuilt). Be sure to do this in the root directory of where the file is.

- Run command to spin up generator and start producing infinite stream of messages: docker-compose up

- Check to make sure everything is up and running as it should: docker exec. follow the command: docker exec -it <mycontainer> bash.

- Verify that I am able to produce messages: kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.transactions --from-beginning

- Verify that I am able to consume messages as legit: kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.legit

- Verify that I am able to consume messages as fraud: kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.fraud
