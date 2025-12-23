# Network Security System

A Machine Learning-based system designed to detect and classify network security threats (specifically phishing) using a comprehensive data pipeline and predictive modeling. This project leverages a robust MLOps workflow, including data ingestion, validation, transformation, model training, and deployment.

## 📖 Project Overview

The **Network Security System** automates the process of identifying malicious network data. It ingests historical phishing data, validates and transforms it, and trains a predictive model. The system exposes the trained model via a **FastAPI** interface for real-time predictions and supports batch prediction through CSV file uploads. It is designed with scalability in mind, utilizing **MongoDB** for data storage and **AWS S3** for artifact management.

## ✨ Key Features
- **End-to-End ML Pipeline**: Automated stages for ingestion, validation, transformation, and training.
- **Real-time & Batch Inference**: API endpoints for triggering training and making predictions on CSV files.
- **Data Validation**: Robust checks for schema validation and data drift using `scikit-learn` and custom logic.
- **MLOps Integration**: Tracks experiments and artifacts using **MLflow** and **DagsHub**.
- **Data Persistence**: efficient data storage and retrieval using **MongoDB Atlas**.
- **Cloud Ready**: Configured for deployment with **Docker** and **AWS**.

## 🛠 Tech Stack

| Category | Tools & Libraries |
|----------|-------------------|
| **Language** | Python 3.10 |
| **Framework** | FastAPI, Uvicorn |
| **Data Processing** | Pandas, NumPy, PyMongo |
| **Machine Learning** | Scikit-learn, Dill |
| **MLOps & Tracking** | MLflow, DagsHub |
| **Infrastructure** | Docker, AWS S3 (Artifacts), MongoDB (Data) |

## 🏗 Architecture & Workflow

1.  **Data Ingestion**: Data is read from CSV/Source, converted to JSON, and stored in **MongoDB**.
2.  **Training Pipeline**:
    *   **Data Ingestion**: Fetches data from MongoDB -> Train/Test split.
    *   **Data Validation**: Validates schema and checks for drift.
    *   **Data Transformation**: Handles missing values (KNN Imputer) and saves preprocessor objects.
    *   **Model Training**: Trains the model and evaluates performance against thresholds.
3.  **Model Registry**: Trained models and preprocessors are saved locally and synced to **AWS S3**.
4.  **Inference**: The FastAPI application loads the model/preprocessor from S3/Local and predicts on new data.

## 📂 Project Structure

```
Network_Security/
├── .github/                # GitHub Actions workflows
├── Network_Data/           # Raw data source (e.g., phisingData.csv)
├── data_schema/            # Schema definition for validation
├── final_model/            # Stores the final production model & preprocessor
├── networksecurity/        # Main package source code
│   ├── cloud/              # Cloud integration (S3 Syncer)
│   ├── components/         # Pipeline components (Ingestion, Validation, etc.)
│   ├── constants/          # detailed Project constants
│   ├── entity/             # Config and Artifact dataclasses
│   ├── exception/          # Custom Exception handling
│   ├── logging/            # Logging configuration
│   ├── pipeline/           # TrainingPipeline logic
│   └── utils/              # Helper utilities
├── prediction_output/      # Stores prediction results
├── templates/              # HTML templates for the web UI
├── app.py                  # FastAPI application entry point
├── main.py                 # Script to trigger the training pipeline manually
├── push_data.py            # Script to seed MongoDB with initial data
├── requirements.txt        # Project dependencies
├── Dockerfile              # Docker image definition
└── setup.py                # Package setup script
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas Account (Connection String)
- AWS Account (Access Keys for S3)

### 1. Clone the Repository
```bash
git clone <repository_url>
cd Network_Security
```

### 2. Create Virtual Environment
```bash
conda create -p venv python=3.10 -y
conda activate ./venv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGODB_URL_KEY="your_mongodb_connection_string"
AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
```

## 🏃 Usage

### Step 1: Push Data to MongoDB
Initialize your database with the provided dataset.
```bash
python push_data.py
```

### Step 2: Run the Training Pipeline
You can trigger the pipeline manually to verify everything is working.
```bash
python main.py
```
*Check logs to see the progress of Ingestion -> Validation -> Transformation -> Training.*

### Step 3: Start the Web App
Launch the FastAPI server.
```bash
python app.py
```
Access the application at `http://localhost:8000`.

## 🔌 API Endpoints

The application provides interactive API documentation at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/` | Redirects to Swagger UI docs. |
| **GET** | `/train` | Triggers the ML training pipeline. Returns success message upon completion. |
| **POST** | `/predict` | Upload a CSV file `{"file": file}`. Returns a table of predictions and saves to `prediction_output/`. |

## 🧠 Data Flow & ML Pipeline

The `TrainingPipeline` class orchestrates the entire process:

1.  **Ingestion**: Connects to MongoDB `NetworkData` collection, exports to CSV, and splits into train/test sets.
2.  **Validation**: Validates data against `data_schema/schema.yaml`. Checks for number of columns and numerical column existence.
3.  **Transformation**: Replaces `NaN` values using `KNNImputer` and standardizes data. Saves the `preprocessor.pkl`.
4.  **Trainer**: Trains a Classification model (e.g., RandomForest/DecisionTree). Saves `model.pkl` if it meets the accuracy threshold (Default: 0.6).
5.  **Sync**: Artifacts are automatically synced to the configured AWS S3 bucket `mysuhasnetworksecurity`.

## 🐳 Deployment

The project includes a `Dockerfile` for containerization.

1.  **Build Docker Image**:
    ```bash
    docker build -t network-security .
    ```
2.  **Run Container**:
    ```bash
    docker run -p 8000:8000 -e MONGODB_URL_KEY="your_key" network-security
    ```
    *(Note: Pass environment variables or mount the `.env` file)*
