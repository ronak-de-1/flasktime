#!/bin/bash

. /functions.sh
# Define the MongoDB connection string
MONGO_CONNECTION_STRING="mongodb://jack:horseman@127.0.0.1:27017/haunted-hallow"

info "Generating Token"
#Static Token
static_token="NoSqueel"

token=$(echo -n ${ATTEMPT_ID}$static_token | md5sum | cut -c 1-6)
static_name="sp00ky-Sk3L3T0N-k3y"


# Define the MongoDB command
MONGO_COMMAND="db.prizes.insert({ image_ref: \"token.jpg\", prize_name: \"${static_name}: ${token}\", required_tokens: 666, quantity: 1, price: 666666 })"

# Function to wait for MongoDB to be up and running
wait_for_mongo() {
    until echo 'db.runCommand({ ping: 1 })' | mongo $MONGO_CONNECTION_STRING --quiet; do
        info "Waiting for MongoDB to start..."
        sleep 1
    done
}

# Function to wait for the "prizes" collection to be created
wait_for_collection() {
    until echo 'db.getCollectionNames().includes("prizes")' | mongo $MONGO_CONNECTION_STRING --quiet | grep -q 'true'; do
        info "Waiting for the 'prizes' collection to be created..."
        sleep 1
    done
}

# Function to connect to MongoDB and execute the command
insert_prize() {
    echo $MONGO_COMMAND | mongo $MONGO_CONNECTION_STRING
    info "Dynamic Token: ${token} added to MongoDB"
}

# Function to run all tasks in sequence
run_all_tasks() {
    wait_for_mongo
    wait_for_collection
    insert_prize
}

# Run the function in the background
run_all_tasks &