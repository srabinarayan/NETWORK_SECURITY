
from pymongo.mongo_client import MongoClient

uri = "mongodb://srabinarayan98:rt0sW7LlOqV5Lt4w@srabinarayan98/?ssl=true&replicaSet=atlas-keotei-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)