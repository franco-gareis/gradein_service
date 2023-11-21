
# GradeIn Service

Exchange service for used equipment, as part of payment for new ones, in physical stores.

## Getting Started

### Dependencies

* Linux/Windows/Mac
* docker >= v24.0.7
* docker-compose >= v2.21.0
* odoo >= v15.0

### Installing

```
* Install odoo from official page
* Install Docker and docker-compose, if not already installed
```

### Executing program

* How to run the program
```
cd /gradein_service
docker compose up
```

## Models

### Equipment Model

The functionality of this model is to create the equipment intended to be used or that have been used in GradeIn orders, Images, prices, and a brief description can be added.

The available fields are:

- Name, Equipment name
- Image, Equipment image
- Active, Whether the equipment is still active to generate an order
- Price, The initial price of the equipment
- Description: A brief description of the equipment being loaded

WARNING: The equipment price cannot be less than or equal to zero, the model includes a validator to ensure this

### Equipment Type Model

This is a model to store all types of equipment that are being created and their information, also you can select multiple questions related to the equipment.

The available fields are:

- Name, Equipment name
- Image, Equipment image
- Active, Whether the equipment is still active to generate an order
- Questions, Questions related to the equipment to generate the order

## Authors

Contributors names

Ariel Montenegro
Yamil Ferrufino
Franco Gareis