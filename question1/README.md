### Question 1
Implementing a CSV to JSON Nifi pipeline.

The README will cover on how to run the Nifi pipeline. For the detailed implementation please check the 'question1.pptx' powerpoint file.

#### Running the pipeline
1. Cd to this directory ('question1')
2. Run ```docker-compose up```
3. Navigate to ```localhost:8080/nifi```
4. Click 'Upload Template' at the NiFi Flow Process Group box on the left
5. Select 'Assignment1.xml'
6. Drag and drop a template from the top left
7. Select 'Assignment1' template
8. Enable the CSVReader and JsonRecordSetWriter Controller Services by clicking on the configuration button (gear) on the Nifi Flow Process Group box on the left then enabling them by clicking the Enable button (lightning bolt) on the right
9. Run the pipeline
10. There should be a converted json file of the csv file inside 'data/data' being created inside 'data/output'