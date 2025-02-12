import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset (assumes dataset.csv contains columns: 'blazer_color', 'shirt_color', 'tie_color', 'shoe_color', 'pant_color')
data = pd.read_csv("dataset.csv")

# Initialize LabelEncoders for each categorical variable.
le_blazer = LabelEncoder()
le_shirt = LabelEncoder()
le_tie = LabelEncoder()
le_shoe = LabelEncoder()
le_pant = LabelEncoder()

# Encode each column.
data['blazer_encoded'] = le_blazer.fit_transform(data['blazer_color'])
data['shirt_encoded'] = le_shirt.fit_transform(data['shirt_color'])
data['tie_encoded'] = le_tie.fit_transform(data['tie_color'])
data['shoe_encoded'] = le_shoe.fit_transform(data['shoe_color'])
data['pant_encoded'] = le_pant.fit_transform(data['pant_color'])

# Define feature. Now includes pant color
X = data[['blazer_encoded', 'pant_encoded']]

# Define targets for each output.
y_shirt = data['shirt_encoded']
y_tie = data['tie_encoded']
y_shoe = data['shoe_encoded']

# Split data into training and testing sets. (Using the same split for all targets.)
X_train, X_test, y_shirt_train, y_shirt_test = train_test_split(X, y_shirt, test_size=0.2, random_state=42)
_, _, y_tie_train, y_tie_test = train_test_split(X, y_tie, test_size=0.2, random_state=42)
_, _, y_shoe_train, y_shoe_test = train_test_split(X, y_shoe, test_size=0.2, random_state=42)

# Train individual RandomForest classifiers.
rf_shirt = RandomForestClassifier(random_state=42)
rf_tie = RandomForestClassifier(random_state=42)
rf_shoe = RandomForestClassifier(random_state=42)

rf_shirt.fit(X_train, y_shirt_train)
rf_tie.fit(X_train, y_tie_train)
rf_shoe.fit(X_train, y_shoe_train)

# Evaluate each model.
shirt_preds = rf_shirt.predict(X_test)
tie_preds = rf_tie.predict(X_test)
shoe_preds = rf_shoe.predict(X_test)

print("Shirt Color Classification Report:")
print(classification_report(y_shirt_test, shirt_preds))
print("Tie Color Classification Report:")
print(classification_report(y_tie_test, tie_preds))
print("Shoe Color Classification Report:")
print(classification_report(y_shoe_test, shoe_preds))

# Function to predict outfit colors given a blazer and pant color input.
def predict_outfit(blazer_color, pant_color):
    try:
        blazer_val = le_blazer.transform([blazer_color])[0]
    except ValueError:
        print(f"Warning: Blazer color '{blazer_color}' not seen during training. Using a default.")
        if 'navy' in le_blazer.classes_:
            blazer_val = le_blazer.transform(['navy'])[0]
        elif len(le_blazer.classes_) > 0:
            blazer_val = le_blazer.transform([le_blazer.classes_[0]])[0]
        else:
            blazer_val = 0

    try:
        pant_val = le_pant.transform([pant_color])[0]
    except ValueError:
        print(f"Warning: Pant color '{pant_color}' not seen during training. Using a default.")
        if 'gray' in le_pant.classes_:
            pant_val = le_pant.transform(['gray'])[0]
        elif len(le_pant.classes_) > 0:
            pant_val = le_pant.transform([le_pant.classes_[0]])[0]
        else:
            pant_val = 0

    shirt_enc = rf_shirt.predict([[blazer_val, pant_val]])[0]
    tie_enc = rf_tie.predict([[blazer_val, pant_val]])[0]
    shoe_enc = rf_shoe.predict([[blazer_val, pant_val]])[0]

    predicted_shirt = le_shirt.inverse_transform([shirt_enc])[0]
    predicted_tie = le_tie.inverse_transform([tie_enc])[0]
    predicted_shoe = le_shoe.inverse_transform([shoe_enc])[0]
    return predicted_shirt, predicted_tie, predicted_shoe

# Example usage:
input_blazer_color = "navy"  # Replace with your input blazer color.
input_pant_color = "gray"  # Replace with your input pant color.
shirt_pred, tie_pred, shoe_pred = predict_outfit(input_blazer_color, input_pant_color)  # Pass both blazer and pant color
print(f"For blazer color '{input_blazer_color}' and pant color '{input_pant_color}', predicted shirt: {shirt_pred}, tie: {tie_pred} and shoe: {shoe_pred}")
print("Done")


