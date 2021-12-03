### Objective
In this tutorial, we will get our hands dirty and create our first streaming application backed by Apache Kafka using a Python client. We will try and make it as close as possible to a real-world Kafka application.


What we'll build is a real-time fraud detection system. We'll do so from scratch. We will
generate a stream of transactions and you will write a Python script to process those stream
of transactions to detect which ones are potential fraud.

### Steps
In order to get the streaming application running, I first needed to create the essential files (app.py, Dockerfile, requirements.txt., transactions.py, docker-compose.kafka.yml and docker-compose.yml files). The steps would then proceed as follows for a successfully running Kafka streaming application:

- Run command to spin up broker and zookeeper: docker-compose -f docker-compose.kafka.yml up -d

- Run command to spin up generator and start producing infinite stream of messages: docker-compose --f docker-compose.yml up

- Check to make sure everything is up and running as it should: docker-compose -f docker-compose.kafka.yml ps docker-compose -f docker-compose.kafka.yml ps

- Run command to log into broker: docker exec -it kafka-frauddetector_broker_1 sh

- Verify that I am able to produce messages: kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.transactions --from-beginning

- Verify that I am able to consume messages as legit: kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.legit

- Verify that I am able to consume messages as fraud: kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.fraud

### Screenshot Info
Attached are screenshots of when I was able to obtain the essential desired queueing.transactions (from generator), legit and fraud messages. I am not always able to have it successfully run, however. For one of the screenshots, I took it before "gracefully exiting" using Ctrl+C.
