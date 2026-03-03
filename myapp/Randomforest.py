# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neural_network import MLPClassifier
# df = pd.read_csv(r'C:\Users\HP\Downloads\untitled3\untitled3\myapp\landslide_dataset.csv')
# X = df.drop('Label', axis=1)
# y = df['Label']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=66)
#
# def random_forest(t1,t2,t3,t4,t5,t6,t7,t8,t9):
#     rfc = RandomForestClassifier()
#     rfc.fit(X_train,y_train)
#     lst=[[t1,t2,t3,t4,t5,t6,t7,t8,t9]]
#     lst=np.array(lst)
#     lst.reshape(-1,1)
#
#     rfc_predict = rfc.predict(lst)
#     print(rfc_predict)
#     ab = rfc.score(X_test, y_test)
#     return str(rfc_predict[0]),ab
#
#
# random_forest(161,32.31153,198.435,0.007029638,-0.012546,9.089893,4.396348,3,1.359568)


import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv(
    r'C:\Users\abhin\Downloads\untitled3\myapp\landslide_dataset.csv'
)

# -------------------------------
# Split features and label
# -------------------------------
X = df.drop('Label', axis=1)
y = df['Label']

# -------------------------------
# Train-test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.33,
    random_state=66
)

# -------------------------------
# Random Forest prediction function
# -------------------------------
def random_forest(t1, t2, t3, t4, t5, t6, t7, t8, t9):
    # Create model
    rfc = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    # Train model
    rfc.fit(X_train, y_train)

    # Create input as DataFrame with correct feature names
    sample = pd.DataFrame(
        [[t1, t2, t3, t4, t5, t6, t7, t8, t9]],
        columns=X.columns
    )

    # Predict
    prediction = rfc.predict(sample)

    # Model accuracy
    accuracy = rfc.score(X_test, y_test)

    return prediction[0], accuracy


# -------------------------------
# Test the function
# -------------------------------
pred, acc = random_forest(
    161,
    32.31153,
    198.435,
    0.007029638,
    -0.012546,
    9.089893,
    4.396348,
    3,
    1.359568
)

print("Prediction:", pred)
print("Model Accuracy:", acc)
