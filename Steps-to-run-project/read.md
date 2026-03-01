🚀 How to Run the Application
Step 1: Install Backend Dependencies
cd backend
pip install -r requirements.txt


Step 2: Train the ML Model
python -m app.model.train_model


Step 3: Start the Backend Server
uvicorn app.main:app --reload


Backend will run at: http://localhost:8000

You can test it at: http://localhost:8000/docs (FastAPI auto-generated docs)


Step 4: Start the Frontend (separate terminal)
cd ../frontend
npm run dev

Frontend will run at: http://localhost:3000
