# Netherite2
Building a cryptocurrency platform for our final year project :)

# Setup<br>
Install Python3 and pip3:<br>
```
sudo apt install python3 -y
sudo apt install python3-pip
```
#Install git and clone repository:<br>
```
sudo apt install git
git clone https://github.com/LoneCannibal/Netherite2/
```

Install requirements: <br>
```
cd Netherite
pip3 install -r requirements.txt
```

# Run blockchain backend:

```
cd blockchain
python3 blockchain.py -p 5001
```

# Run blockchain frontend:
> :warning: Open a new terminal window and go to the parent directory!
```
cd client
python3 blockchain_client.py -p 8081
```


# Access web application

Copy paste the following links in your browser

Backend:
```
http://localhost:5001
```
<br>

Frontend:
```
http://localhost:8081
```
