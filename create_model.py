import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle

# Örnek veri oluştur
np.random.seed(42)
n_samples = 1000

# Özellikler
temp = np.random.normal(20, 10, n_samples)
humidity = np.random.normal(60, 20, n_samples)
pm25 = np.random.exponential(30, n_samples)
pm10 = np.random.exponential(50, n_samples)
no2 = np.random.exponential(40, n_samples)
so2 = np.random.exponential(20, n_samples)
co = np.random.exponential(3, n_samples)
industrial_distance = np.random.uniform(1, 50, n_samples)

# Hedef değişken oluştur (hava kalitesi)
# 0: İyi, 1: Orta, 2: Kötü
air_quality = []
for i in range(n_samples):
    score = (pm25[i] * 0.3 + pm10[i] * 0.2 + no2[i] * 0.2 + so2[i] * 0.1 + 
             co[i] * 0.1 + humidity[i] * 0.05 + temp[i] * 0.05 - industrial_distance[i] * 0.5)
    
    if score < 30:
        air_quality.append(0)  # İyi
    elif score < 70:
        air_quality.append(1)  # Orta
    else:
        air_quality.append(2)  # Kötü

# DataFrame oluştur
df = pd.DataFrame({
    'temp': temp,
    'humidity': humidity,
    'pm25': pm25,
    'pm10': pm10,
    'no2': no2,
    'so2': so2,
    'co': co,
    'industrial_distance': industrial_distance,
    'air_quality': air_quality
})

# Özellikler ve hedef
X = df[['temp', 'humidity', 'pm25', 'pm10', 'no2', 'so2', 'co', 'industrial_distance']]
y = df['air_quality']

# Veriyi böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model eğit
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Modeli kaydet
with open('dataset/logreg_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model başarıyla oluşturuldu ve kaydedildi!")
print(f"Model doğruluğu: {model.score(X_test_scaled, y_test):.2f}")
