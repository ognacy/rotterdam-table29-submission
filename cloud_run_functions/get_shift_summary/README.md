# Get Shift Summary Cloud Run Function

This directory contains a Cloud Run function that provides a summary of a patient's shift.

## Functionality

This function is triggered by an HTTP request and does the following:

1.  Retrieves the patient's shift data from the database.
2.  Generates a summary of the shift, including activities, meals, and medications.
3.  Returns the summary as a JSON response.

## Deployment

This function can be deployed to Google Cloud Run. The `requirements.txt` file lists the required Python packages.
