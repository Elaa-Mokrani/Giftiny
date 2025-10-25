from pyspark.sql import SparkSession

# Créer la session Spark avec la connexion à MongoDB
spark = SparkSession.builder \
    .appName("GiftRecommendationSpark") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1/gift_recommendation.gifts") \
    .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1/gift_recommendation.recommendations") \
    .getOrCreate()

# Lire les données de la collection MongoDB
gifts_df = spark.read.format("mongodb").load()

# Afficher les 5 premières lignes
gifts_df.show(5)
