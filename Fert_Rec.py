from sklearn.model_selection import KFold, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
import numpy as np
import warnings
from sklearn.exceptions import UndefinedMetricWarning
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# Load the data
data = pd.read_csv("Cleaned Fertilizer Prediction.csv")

# Create a label encoder for each column
crop_type_encoder = LabelEncoder()
fertilizer_name_encoder = LabelEncoder()
soil_type_encoder = LabelEncoder()

# Encode non-numeric columns
data["Crop Type"] = crop_type_encoder.fit_transform(data["Crop Type"])
data["Fertilizer Name"] = fertilizer_name_encoder.fit_transform(data["Fertilizer Name"])
data["Soil Type"] = soil_type_encoder.fit_transform(data["Soil Type"])

# Split the data into features and target variables
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Define the SVM model
svc_model = SVC()

# Define the parameter grid for GridSearchCV
param_grid = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001]}

# Create a k-fold cross-validation object with 5 folds
kf = KFold(n_splits=5)
# Create empty lists to store the scores and predictions on each fold
scores = []
predictions = []

# Loop over each fold
for train_idx, test_idx in kf.split(X):
    # Split the data into training and test sets for this fold
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    # Fit the model on the training data
    grid = GridSearchCV(svc_model, param_grid, refit=True, verbose=2)
    grid.fit(X_train, y_train)

    # Make predictions on the test data
    fold_predictions = grid.predict(X_test)
    predictions.append(fold_predictions)

    # Compute the accuracy score for this fold
    fold_accuracy = accuracy_score(y_test, fold_predictions)
    scores.append(fold_accuracy)

# Compute the mean accuracy score across all folds
mean_accuracy = sum(scores) / len(scores)
print("Mean accuracy score:", mean_accuracy)

# Compute the overall confusion matrix and classification report across all folds
all_predictions = np.concatenate(predictions)
conf_matrix = confusion_matrix(y, all_predictions)
class_report = classification_report(y, all_predictions)

print("Overall confusion matrix:")
print(conf_matrix)
print("Overall classification report:")
print(class_report)

overall_accuracy = accuracy_score(y, all_predictions)
print("Overall accuracy score:", overall_accuracy)