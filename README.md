<p align="center">
    <img src="https://github.com/user-attachments/assets/e514785d-3777-481c-ba46-f81168892f95" alt="wt_logo">
</p>

> Platform to enhance your English writing level.

## What is the project?

The project is a platform designed to enhance the English level of developers by tracking their proficiency in common professional situations, such as reporting daily progress to a tech lead.

Each user can view their metrics and reviews of each test (features under development).

The project was developed using the Streamlit framework for the frontend (a Python library) and Flask for the backend. MongoDB is used as the database, and everything is hosted on Render (both frontend and backend).

The project can be accessed at: [writing-test-front.onrender.com](https://writing-test-front.onrender.com/)

All credentials are created by the responsible developer for this project [@Edu-p](https://github.com/Edu-p), but to test you can use:
- Email: `github_test_email@test.com`
- Password: `just_testing`

## Technical Description

To run the project locally, you will need to set up the following environment variables:

### Backend
- **MONGO_URI**: Your MongoDB connection URI.
- **OPENAI_API_KEY**: Your OpenAI API key.

### Execution Instructions

**Frontend:**

```bash
# Navigate to the frontend directory
cd streamlit_frontend

# Run the frontend
streamlit run app.py
```

**Backend:**

```bash
# Navigate to the backend directory
cd flask_backend

# Run the backend
python app.py
