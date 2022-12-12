# Calculate Rolling Average for Bitcoin Price in Euro. 

Python App to calculate rolling average in EUR for bitcoin price for the year 2021. Uses Messari API to fetch bitcoin price and uses reference data from Euro to calculate the average. 

### Outputs

- CSV containing rolling average including nulls. 
    - data_output/USD_EUR_bitcoin_roll_avg_2021.csv
- visualization showing the trend of 7 day rolling avg with price in USD & EUR. 
    - rolling_average_picture.png

### Running the application

```python
python calculate_rolling.py 'data/eurofxref-hist.csv' 'bitcoin' 'price' '2021' 'USD' '2021-01-01' '2021-12-31'
```

Script followed by
- **reference file name** containing USD to EUR exchange rate
- **token** as expected by messari api
- **metric** as expected by messari api
- **year** for which the average is calculated
- **base currency** for conversion
- **min date** range for the request
- **max date** range for the request

### Design & Approach

- Separate module for API Interaction which provides extensibility to fetch data from other end points. 
- Average calculation and Input are coupled in the same script but handled separately. 
- Source data can be staged before compute to provide the ability to perform multiple reads to the as needed.
- backend data store provides flexibility to perform adhoc querying, connect data store to BI tools.

Here is the high level design for the app

More unit test cases should be added to relevant scripts to cover base functionality (added few relevant ones in messari.py)

![High level design](/high_level_design.png)

### Production Considerations & deployment

Considering this application will be executed daily and the complexity, serverless deployment like lambda could be faster and easier to maintain. Here are some patterns based on some assumptions

- Assumptions
    - Daily fetch for the current day
    - this application to calculate rolling average is maintained separately
    - we are clear with known issues around API, Cloud environment

- Requirements
    - Functional
        - Ability to Calculate 7 day rolling average in EURO
        - Ability to generate data visualization picture if required.
        - Ability to fetch right token data from Messari API
    - Non functional
        - Low latency
        - Consistency over availability

- Deployment
    - AWS Serverless deployment to run the app via Lambda (s3 & RDS can used as data store before and after compute)
        - this can be done via make file and aws cli and can be pipelined via Jenkins
        - Sample deployment pipeline using aws cli can be found [here](https://github.com/Anandkarthick/aws_pipeline_example)
        - cloudformation stacks and policies with jenkins
        - Github actions or Circle CI deployment to create a packge and deploy as lambda function
        - Schedule the job to run according to cron schedule
    - Airflow
        - If there is a Airflow instance that's set up with deployment already then this can simply be a DAG and reuable API components can be shared across to be utilized by any other DAG or Tasks
    
