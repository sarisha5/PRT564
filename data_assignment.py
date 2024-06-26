import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'F:\Assignment CDU SEM 1\Data Visualization\Data Visualisation Code\groupASScode\retractions35215.csv')

df.info()

df.head()

# Visualize missing values
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cmap='viridis', cbar=True)
plt.title('Missing Values Heatmap')
plt.show()

# Convert date columns to datetime format
df['RetractionDate'] = pd.to_datetime(df['RetractionDate'], format='%m/%d/%Y', errors='coerce')
df['OriginalPaperDate'] = pd.to_datetime(df['OriginalPaperDate'], format='%m/%d/%Y', errors='coerce')

df = df.dropna(subset=['RetractionDate', 'OriginalPaperDate'])

df['is_retracted'] = 1

df['years_to_retraction'] = (df['RetractionDate'] - df['OriginalPaperDate']).dt.days / 365.25

features = df[['CitationCount', 'years_to_retraction']]

# Drop rows with missing values in features
features = features.dropna()

# Define the target
target = df.loc[features.index, 'is_retracted']

# Plot the distribution of citation counts
plt.figure(figsize=(10, 6))
sns.histplot(df['CitationCount'], kde=True, bins=30)
plt.title('Distribution of Citation Counts')
plt.xlabel('Citation Count')
plt.ylabel('Frequency')
plt.show()

# Plot the distribution of years to retraction
plt.figure(figsize=(10, 6))
sns.histplot(df['years_to_retraction'], kde=True, bins=30)
plt.title('Distribution of Years to Retraction')
plt.xlabel('Years to Retraction')
plt.ylabel('Frequency')
plt.show()

# Feature scaling
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Dimensionality reduction with PCA
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)

# Pairplot to visualize the relationships between features
sns.pairplot(df[['CitationCount', 'years_to_retraction', 'is_retracted']])
plt.suptitle('Pairplot of Selected Features', y=1.02)
plt.show()

correlation_matrix = df[['CitationCount', 'years_to_retraction', 'is_retracted']].corr()

# Visualize the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Scatter plot of Citation Count vs. Years to Retraction
plt.figure(figsize=(10, 6))
plt.scatter(df['CitationCount'], df['years_to_retraction'], alpha=0.5, c='blue')
plt.title('Citation Count vs. Years to Retraction')
plt.xlabel('Citation Count')
plt.ylabel('Years to Retraction')
plt.show()

# Feature scaling
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Dimensionality reduction with PCA
pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)

# PCA visualization
plt.figure(figsize=(10, 6))
plt.scatter(features_pca[:, 0], features_pca[:, 1], c=target, cmap='viridis', alpha=0.5)
plt.title('PCA of Retraction Data Before Modeling')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar()
plt.show()

# Create a synthetic negative class
num_samples = len(features)
synthetic_data = np.random.randn(num_samples, features.shape[1])
synthetic_target = np.zeros(num_samples)

# Combine real and synthetic data
combined_features = np.vstack((features, synthetic_data))
combined_target = np.hstack((target, synthetic_target))

# Convert to DataFrame
combined_df = pd.DataFrame(combined_features, columns=features.columns)
combined_target = pd.Series(combined_target, name='is_retracted')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(combined_df, combined_target, test_size=0.3, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
# Train the model
lr_model = LogisticRegression()
lr_model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_lr = lr_model.predict(X_test_scaled)

# Evaluate the model
accuracy_lr = accuracy_score(y_test, y_pred_lr)
recall_lr = recall_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr)
conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)

# Print the results
print(f"Linear Regression:\nAccuracy: {accuracy_lr}\nRecall: {recall_lr}\nPrecision: {precision_lr}\nF1 Score: {f1_lr}")
print(f"Confusion Matrix:\n {conf_matrix_lr}")

from sklearn.naive_bayes import GaussianNB

# Train the model
nb_model = GaussianNB()
nb_model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_nb = nb_model.predict(X_test_scaled)

# Evaluate the model
accuracy_nb = accuracy_score(y_test, y_pred_nb)
recall_nb = recall_score(y_test, y_pred_nb)
precision_nb = precision_score(y_test, y_pred_nb)
f1_nb = f1_score(y_test, y_pred_nb)
conf_matrix_nb = confusion_matrix(y_test, y_pred_nb)

# Print the results
print(f"Naive Bayes:\nAccuracy: {accuracy_nb}\nRecall: {recall_nb}\nPrecision: {precision_nb}\nF1 Score: {f1_nb}")
print(f"Confusion Matrix:\n {conf_matrix_nb}")

from sklearn.cluster import KMeans

# Train the model
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_train_scaled)

# Predict on the test set
y_pred_kmeans = kmeans.predict(X_test_scaled)

# Adjust cluster labels to match target labels
y_pred_kmeans = np.where(y_pred_kmeans == 0, 1, 0)

# Evaluate the model
accuracy_kmeans = accuracy_score(y_test, y_pred_kmeans)
recall_kmeans = recall_score(y_test, y_pred_kmeans)
precision_kmeans = precision_score(y_test, y_pred_kmeans)
f1_kmeans = f1_score(y_test, y_pred_kmeans)
conf_matrix_kmeans = confusion_matrix(y_test, y_pred_kmeans)

# Print the results
print(f"K-Means Clustering:\nAccuracy: {accuracy_kmeans}\nRecall: {recall_kmeans}\nPrecision: {precision_kmeans}\nF1 Score: {f1_kmeans}")
print(f"Confusion Matrix:\n {conf_matrix_kmeans}")

from sklearn.tree import DecisionTreeClassifier

# Train the model
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train_scaled, y_train)

# Predict on the test set
y_pred_dt = dt_model.predict(X_test_scaled)

# Evaluate the model
accuracy_dt = accuracy_score(y_test, y_pred_dt)
recall_dt = recall_score(y_test, y_pred_dt)
precision_dt = precision_score(y_test, y_pred_dt)
f1_dt = f1_score(y_test, y_pred_dt)
conf_matrix_dt = confusion_matrix(y_test, y_pred_dt)

# Print the results
print(f"Decision Tree:\nAccuracy: {accuracy_dt}\nRecall: {recall_dt}\nPrecision: {precision_dt}\nF1 Score: {f1_dt}")
print(f"Confusion Matrix:\n {conf_matrix_dt}")

from sklearn.svm import SVC

# Linear Kernel
svm_linear = SVC(kernel='linear', random_state=42)
svm_linear.fit(X_train_scaled, y_train)
y_pred_svm_linear = svm_linear.predict(X_test_scaled)
accuracy_svm_linear = accuracy_score(y_test, y_pred_svm_linear)
recall_svm_linear = recall_score(y_test, y_pred_svm_linear)
precision_svm_linear = precision_score(y_test, y_pred_svm_linear)
f1_svm_linear = f1_score(y_test, y_pred_svm_linear)
conf_matrix_svm_linear = confusion_matrix(y_test, y_pred_svm_linear)

print(f"SVM with Linear Kernel:\nAccuracy: {accuracy_svm_linear}\nRecall: {recall_svm_linear}\nPrecision: {precision_svm_linear}\nF1 Score: {f1_svm_linear}")
print(f"Confusion Matrix:\n {conf_matrix_svm_linear}")

# RBF Kernel
svm_rbf = SVC(kernel='rbf', random_state=42)
svm_rbf.fit(X_train_scaled, y_train)
y_pred_svm_rbf = svm_rbf.predict(X_test_scaled)
accuracy_svm_rbf = accuracy_score(y_test, y_pred_svm_rbf)
recall_svm_rbf = recall_score(y_test, y_pred_svm_rbf)
precision_svm_rbf = precision_score(y_test, y_pred_svm_rbf)
f1_svm_rbf = f1_score(y_test, y_pred_svm_rbf)
conf_matrix_svm_rbf = confusion_matrix(y_test, y_pred_svm_rbf)

print(f"SVM with RBF Kernel:\nAccuracy: {accuracy_svm_rbf}\nRecall: {recall_svm_rbf}\nPrecision: {precision_svm_rbf}\nF1 Score: {f1_svm_rbf}")
print(f"Confusion Matrix:\n {conf_matrix_svm_rbf}")

# Polynomial Kernel
svm_poly = SVC(kernel='poly', degree=3, random_state=42)
svm_poly.fit(X_train_scaled, y_train)
y_pred_svm_poly = svm_poly.predict(X_test_scaled)
accuracy_svm_poly = accuracy_score(y_test, y_pred_svm_poly)
recall_svm_poly = recall_score(y_test, y_pred_svm_poly)
precision_svm_poly = precision_score(y_test, y_pred_svm_poly)
f1_svm_poly = f1_score(y_test, y_pred_svm_poly)
conf_matrix_svm_poly = confusion_matrix(y_test, y_pred_svm_poly)

print(f"SVM with Polynomial Kernel:\nAccuracy: {accuracy_svm_poly}\nRecall: {recall_svm_poly}\nPrecision: {precision_svm_poly}\nF1 Score: {f1_svm_poly}")
print(f"Confusion Matrix:\n {conf_matrix_svm_poly}")

# Create a mesh to plot the decision boundaries
h = .02  # step size in the mesh
x_min, x_max = features_pca[:, 0].min() - 1, features_pca[:, 0].max() + 1
y_min, y_max = features_pca[:, 1].min() - 1, features_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

conf_matrix = confusion_matrix(y_test, y_pred_nb)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for Naive Bayes')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_lr = confusion_matrix(y_test, y_pred_lr)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_lr, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for Logistic Regression')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_kmeans = confusion_matrix(y_test, y_pred_kmeans)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_kmeans, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for K-Means Clustering')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_dt = confusion_matrix(y_test, y_pred_dt)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_dt, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for Decision Tree')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_svm_linear = confusion_matrix(y_test, y_pred_svm_linear)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_svm_linear, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for SVM (Linear Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_svm_rbf = confusion_matrix(y_test, y_pred_svm_rbf)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_svm_rbf, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for SVM (RBF Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

conf_matrix_svm_poly = confusion_matrix(y_test, y_pred_svm_poly)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix_svm_poly, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix for SVM (Polynomial Kernel)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
