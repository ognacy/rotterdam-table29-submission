![Banner](banner.png)

# Rotterdam Table 29 Submission

This repository contains three agents and supporting functions.

Those agents are supporting parents with special-needs children - those that require 24/7 support from medical professionals and doctors.

The three agents support 
(1) the parents - allowing them to more easily communicate with caregivers, record instructions, monitor status and manage their schedules
(2) the caregivers - allowing them to ask about care instructions, pass information about meals, meds, activities from one shift to another, and review notes left by the previous shift
(3) the doctors - by giving them an easy way to review past data, care notes left by the nurses and parents. 

Here is our plan:

![Banner](the_plan.png)


## Agents

### 1. Caregiver Agent

The `caregiver/` directory contains an agent that acts as a caregiver. This agent is responsible for logging information about the patient, such as activities, meals, and medications.

### 2. Parent Agent

The `parent/` directory will contain an agent that acts as a parent. This agent will be able to query the system for information about the patient.

### 3. Doctor and Parent Medical Documentation Agent

The `doctor/` directory will contain an agent that can be used by doctors and parents to access medical documentation.

### 4. Patient Logger Agent

The `patient_logger_agent/` directory contains an agent that is responsible for logging patient information. The agent works by interviewing caregivers with a set of questions to create a daily, highly informative session log. This structured data capture ensures that all critical aspects of the patient's day are recorded.

![Caregiver Interview](caregiver_interview.png)

Practitioners, such as doctors or new caregivers, can then ask questions about the patient in natural language. The agent will analyze the logs and provide detailed answers, making it easy to access relevant information and understand the patient's history and progress.

![Practitioner Exploratory Information Discovery](practitioner_exploratory_information_discovery.png)

## Supporting Functions

### Cloud Run Functions

The `cloud_run_functions/` directory contains a Cloud Run function that is responsible for providing a summary of the patient's shift.

This repository also contains supporting functions used by the agents.
