# recommender.py
import pymongo
from collections import Counter

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gift_recommendation"]
gifts_col = db["gifts"]
reco_col = db["recommendations"]  # pour sauvegarder

def score_gift(user, gift, weights=None):
    # user: dict with keys age, gender, interests(list), favorite_color, budget (optional)
    # gift: document from MongoDB
    if weights is None:
        weights = {"tags": 0.5, "age": 0.2, "gender": 0.15, "color": 0.15}
    score = 0.0

    # 1) tags / interests overlap
    user_tags = set([i.lower() for i in user.get("interests", [])])
    gift_tags = set([t.lower() for t in gift.get("tags", [])])
    if user_tags and gift_tags:
        overlap = len(user_tags & gift_tags) / max(len(user_tags), 1)
        score += weights["tags"] * overlap

    # 2) age match (binary or distance)
    age = user.get("age")
    age_range = gift.get("age_range", [0, 100])
    if age is not None:
        if age_range[0] <= age <= age_range[1]:
            score += weights["age"] * 1.0
        else:
            # petit score si pas dedans (distance normalisée)
            dist = min(abs(age - age_range[0]), abs(age - age_range[1]))
            # cap et inverse -> plus la distance est grande, moins le score
            score += weights["age"] * max(0, 1 - dist/100)

    # 3) gender match
    genders = [g.lower() for g in gift.get("gender", [])]
    user_gender = user.get("gender", "").lower()
    if not genders or user_gender in genders:
        score += weights["gender"] * 1.0
    else:
        score += weights["gender"] * 0.0

    # 4) color preference (binary)
    fav = user.get("favorite_color", "").lower()
    gift_colors = [c.lower() for c in gift.get("colors", [])]
    if fav and any(fav in c for c in gift_colors):
        score += weights["color"] * 1.0

    # Optionnel : budget / price matching (non implémenté ici)
    return round(score, 4)

def recommend(user, top_n=5):
    cursor = gifts_col.find({})
    scored = []
    for g in cursor:
        s = score_gift(user, g)
        scored.append((g, s))
    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)
    top = scored_sorted[:top_n]

    # sauvegarder recommandations
    reco_doc = {
        "user": user,
        "recommendations": [{"gift_id": g["gift_id"], "name": g["name"], "score": score} for g, score in top]
    }
    reco_col.insert_one(reco_doc)
    return reco_doc["recommendations"]
