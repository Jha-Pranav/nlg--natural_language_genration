
1. Install gramex 
>> conda create -y --name gramex python=3.7            # Create a new environment
>> conda activate gramex                               # Activate it
>> conda install -y -c conda-forge -c gramener gramex  # Install Gramex
>> gramex setup --all 

2. Install dependencies
>> pip install -r requirments.txt
3. Go to path ../nlg-service/app/
>> gramex
4. open in browser:
localhost:9988/backup/policy_complaint/policy_changes