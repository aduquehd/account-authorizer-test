# Account Authorizer

## Description

Account Authorizer is an "authorizer transactions events".

It's built on Python 3.7 and implemented on Docker, so it's very easy to use.

Every method involved in the behavior of the account authorizer application has a unit test with a high coverage 
percentage.

The methods are very sorted, following the single responsibility principle.

Python is not very natural with functional programming but I implemented some immutable objects (like the Account
management) and some functional programming practices (like, functions as reference). I was very careful with the
account and transaction state to doesn't update it on the way (Trying to follow the FP rules).

## Application structure

The distribution of the application is this:

The src directory contains all the application files, split by handlers and utilities. Also, the handlers and utilities
are split by common functionalities.

The utilities contains the shared methods used in more than one place.

The test directory contains all the tests split by functionality (handlers and utilities.)

- src/
    - handlers/
    - utils/
    - account_authorizer.py
- test/
    - account_authorizer/
        - handlers/
        - utils/



## Running the application & Unit Tests

### Build the docker image

`docker build -t account_authorizer .`

### Run Unit Tests
`docker run -it account_authorizer /bin/bash -c "python -m pytest"`

# Execute the account authorizer
`cat operations | docker run -i account_authorizer`

~ Note: operations is the name of the file with the operations (See an example below).
---

### Operations example:
```json
{"account": {"active-card": true, "available-limit": 100}}
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
{"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:00:00.000Z"}}
```
