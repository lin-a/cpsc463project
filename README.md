# cpsc463project_feature2  
This  project is for the description here:  
`2. Car dealerships need new software to order new cars from the car manufacturer. The dealerships only have so much space in their lots, depending on how big of a dealership they own.` 
Demo on [YouTube](https://youtu.be/AaVoTvrTR4A) in case this project doesn't work on your computer.
# Requirements
MySQL 8.0  
Python3  
Internet Browser(tested in Microsoft Edge)  
IDE (This is optional, tested with PyCharm CE)
# Setup  
1. Download this repository  
2. In the database folder, you can use the createdb.sql to create the database (edit db.yaml accordingly), the other files are for import, not needed  
3. Keep the rest of files in the same directory  
4. Install the required libraries(Flask, Flask_mysql) through requirements.txt `pip install -r requirements.txt`  
  4a. If it does not work do `pip install flask` and `pip install flask-mysql`  
5. To start the web service `python app.py`  
6. Start up internet browser and go to the address `http://localhost:5000/`  
  
That's all for the setup
