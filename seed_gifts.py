# seed_gifts.py
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gift_recommendation"]
gifts = db["gifts"]

# Nettoie si besoin
gifts.delete_many({})

sample_gifts = [
    {"gift_id": 1, "name": "Smartwatch", "category": "Technology", "tags": ["tech","fitness"], "gender": ["Male","Other"], "age_range": [18, 50], "price": 120, "colors": ["black","silver"]},
    {"gift_id": 2, "name": "Perfume Set", "category": "Fashion", "tags": ["beauty","luxury"], "gender": ["Female"], "age_range": [20, 60], "price": 60, "colors": ["pink","gold"]},
    {"gift_id": 3, "name": "Novel - Best Seller", "category": "Books", "tags": ["books","literature"], "gender": ["Female","Male","Other"], "age_range": [15, 80], "price": 20, "colors": []},
    {"gift_id": 4, "name": "Watercolor Kit", "category": "Art", "tags": ["creative","art"], "gender": ["Female","Other"], "age_range": [10, 70], "price": 35, "colors": ["blue","green"]},
    {"gift_id": 5, "name": "Wireless Earbuds", "category": "Technology", "tags": ["music","tech"], "gender": ["Male","Female","Other"], "age_range": [15, 45], "price": 80, "colors": ["white","black"]},
    {"gift_id": 6, "name": "Personalized Mug", "category": "Home", "tags": ["custom","practical"], "gender": ["Male","Female","Other"], "age_range": [10, 80], "price": 15, "colors": ["white","red"]},
    # ajoute autant d'exemples que tu veux...
]

gifts.insert_many(sample_gifts)
print("Seed done.")
