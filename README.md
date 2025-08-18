# Air-Sense: Urban Air Quality Prediction AI Agent

## 🚀 Project Overview

Air-Sense is a cutting-edge project designed to combat the critical issue of urban air pollution by leveraging the power of data and artificial intelligence. Our project goes beyond simply monitoring air quality; it acts as a **proactive early warning system** by predicting future pollution levels.

The core idea is to move from passive data monitoring to active, predictive insights, empowering individuals and urban authorities to make informed decisions for a healthier community.

## App
👉🏻 [**Air-Sense: Urban Air Quality Prediction App**](https://gulcihanglmz-urban-air-quality-ozone-value-streamlit-app-nu3fsx.streamlit.app/)


## ✨ Features

- **Hybrid Prediction Model:** We utilize a two-pronged approach with two distinct models to address different problem scales:
    1.  **Short-Term Prediction:** Predicts air quality for the next 24-48 hours based on real-time factors like temperature and traffic density.
    2.  **Long-Term Analysis:** Analyzes a city's structural features (e.g., population density, proximity to industrial zones) to forecast long-term air quality trends.

- **AI Agent-Based Early Warning:** The project's "AI Agent" component automatically processes the model's predictions. When a critical pollution threshold is expected to be crossed, the agent triggers an instant alert, notifying at-risk groups (individuals with asthma, chronic illnesses, etc.).

- **Multi-Factor Analysis:** Our models are trained on diverse datasets, including air quality, weather, and traffic data, allowing us to capture complex, non-linear relationships that influence pollution levels.

- **Scalable Architecture:** Designed to be adaptable to different cities and data sources, demonstrating its potential for widespread application.

## 🛠️ Tech Stack

- **Language:** Python
- **Data Analysis:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn` (for RandomForestRegressor), `tensorflow` or `keras` (for LSTM)
- **Data Visualization:** `matplotlib`, `seaborn`
- **Application Framework:** `Streamlit` or `Dash` (for the user interface)

## 📊 Data

We utilized data from multiple Kaggle datasets to build and validate our models:
- **[General City Data](https://www.kaggle.com/datasets/mujtabamatin/air-quality-and-pollution-assessment):** A broader dataset including air pollution metrics, population, and industrial factors for cities like Tehran.

A key challenge was integrating datasets with different date ranges and temporal frequencies. Our solution involved sophisticated data engineering to extract meaningful features that could be fed into our models.

## 📦 Installation & Usage

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/gulcihanglmz/Airsense-Urban-Smart-Air-Quality-Forecast-System
    ```
    
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: You'll need to create a `requirements.txt` file with your installed libraries.)
    
3.  **Run the App:**
    ```bash
    streamlit run app_file.py
    ```
    
## 👥 Team

- [**Gülcihan Gülmez**](https://github.com/gulcihanglmz): Project Manager & Data Analysis & Machine Learning
- [**Mustafa Enes Güzelordu**](https://github.com/menesgo): Data Preprocessing & Model Design for Machine Learning
- [**Berke Ateş**](https://github.com/berkeatesh): Dataset Analyst & Storage, Interface Design
- [**Pedram Shahriyari**](https://github.com/pedramsh01): Developer & UX Designer & Healthcare Professional

## 🗺️ Roadmap

Our future plans for Air-Sense include:
- Integrating a real-time data streaming pipeline for live predictions.
- Developing a user interface.
- Expanding the model's scope to cover more cities and a wider range of pollutants.
- Incorporating satellite imagery data for more accurate and localized predictions.

---
🩵 Thank you for your interest in Air-Sense! Feel free to reach out to our team with any questions or feedback.
