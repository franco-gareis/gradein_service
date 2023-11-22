
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

![Equipment Form](/addons/gradein/images/equipment_form.png?raw=true)
![Equipment Tree](/addons/gradein/images/equipment_tree.png?raw=true)

### Equipment Type Model

This is a model to store all types of equipment that are being created and their information, also you can select multiple questions related to the equipment.

The available fields are:

- Name, Equipment name
- Image, Equipment image
- Active, Whether the equipment is still active to generate an order
- Questions, Questions related to the equipment to generate the order

![Equipment Type Form](/addons/gradein/images/equipment_type_form.png?raw=true)
![Equipment Type Tree](/addons/gradein/images/equipment_type_tree.png?raw=true)

## GradeIn Answer

### Model

The functionality of this model is to create selectable answers for a question.

The available fields are:

- Name, Answer name.
- Price reduction, Price to be deducted from the total budget.
- Blocking, If true, the form is blocked.
- Active, If the answer is active to be assigned to a question.

## Images

### Menu
![Equipment Type Form](/addons/gradein/images/gradein_answer/gradein_answer_menu.png?raw=true)
### List
![Equipment Type Form](/addons/gradein/images/gradein_answer/gradein_answer_view_tree.png?raw=true)
### Form
![Equipment Type Form](/addons/gradein/images/gradein_answer/gradein_answer_view_form.png?raw=true)

# GradeIn questions

### Model

The class GradeInQuestion is an Odoo model representing survey questions. It has the following fields:

    name: A Char field representing the question's name.
    active: A Boolean field indicating if the question is active.
    equipment_type_ids: A Many2many field representing the associated equipment types.
    answer_ids: A One2many field representing the possible answers associated with the question.

## Images

### Menu
![Question Type Form](/addons/gradein/images/gradein_question/gradein_question_form.png?raw=true)
### List
![Question Type List](/addons/gradein/images/gradein_question/gradein_question_list.png?raw=true)
### Form
![Question Type Search](/addons/gradein/images/gradein_question/gradein_question_search.png?raw=true)


## Authors

Contributors names

Ariel Montenegro
Yamil Ferrufino
Franco Gareis

