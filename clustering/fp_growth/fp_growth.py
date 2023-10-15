from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth

def fp_growth(data, min_support=0.5, min_confidence=0.6, show=False):
    # Create the Spark session
    spark = SparkSession.builder \
        .appName("FP-growth") \
        .getOrCreate()

    # Convert data to DataFrame
    df = spark.createDataFrame(data, ["id", "items"])

    # Set the FP-growth
    fp_growth = FPGrowth(itemsCol="items", minSupport=min_support, minConfidence=min_confidence)

    # Train the model
    model = fp_growth.fit(df)

    # Output
    print(f"min_support: {min_support}, min_confidence: {min_confidence}")
    if show:
        model.freqItemsets.show()
        return None
    else:
        frequent_itemsets = model.freqItemsets.collect()
        output = [{'freq': row['freq'], 'item': row['items']} for row in frequent_itemsets]
        return output


    # Generate the association rules
    # association_rules = model.associationRules
    # association_rules.show()

    # Stop the Spark session
    spark.stop()
