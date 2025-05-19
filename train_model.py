import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv('dataset_toko.csv')

# Fitur dan Label
X = df[['jumlah_ulasan', 'avg_rating']]  # Fitur: jumlah ulasan dan avg rating
y = df['status_rekomendasi']  # Label: status rekomendasi

# Split data menjadi train dan test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inisialisasi dan latih model Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Prediksi dan evaluasi model
y_pred = model.predict(X_test)
print("Akurasi:", accuracy_score(y_test, y_pred))

# Simpan model untuk digunakan di Flask
joblib.dump(model, 'model/logistic_model.pkl')
