# 🔗 My Classroom

**My Classroom** is a lightweight classroom networking web app built
with Streamlit.\
It allows students to add their LinkedIn usernames and instantly access
each other's profiles through a clean shared directory.

The goal is simple:\
👉 make classroom networking frictionless\
👉 avoid searching names manually\
👉 build professional connections faster

------------------------------------------------------------------------

## ✨ Features

-   👤 Students add their name + LinkedIn username\
-   🔗 Automatic LinkedIn profile link generation\
-   📚 Clean searchable classroom directory\
-   📈 Real-time analytics dashboard\
-   🔐 Admin-only CSV export\
-   ⚡ Optimized for fast Streamlit Cloud deployment\
-   🎨 Minimal, modern UI using native Streamlit components

------------------------------------------------------------------------

## 🧠 How It Works

1.  A user enters:
    -   Full name
    -   LinkedIn username
2.  The app builds their profile URL automatically:

```{=html}
<!-- -->
```
    https://www.linkedin.com/in/{username}

3.  All users appear in a shared directory\
4.  Anyone can click a name to open their LinkedIn profile

------------------------------------------------------------------------

## 🏗️ Project Structure

    MyConnections/
    │
    ├── app.py
    ├── config/settings.py
    ├── database/
    │   ├── mongo.py
    │   └── user_repo.py
    ├── services/
    │   ├── user_service.py
    │   └── analytics_service.py
    ├── ui/
    │   ├── add_user.py
    │   ├── dashboard.py
    │   └── analytics.py
    ├── utils/auth.py
    └── requirements.txt

------------------------------------------------------------------------

## 🚀 Deployment (Streamlit Community Cloud)

1.  Push your repo to GitHub\
2.  Go to https://share.streamlit.io/\
3.  Click **New App**\
4.  Select your repo and choose `app.py`

------------------------------------------------------------------------

### 🔐 Add Secrets

In Streamlit Cloud → App Settings → Secrets

    MONGO_URI="your_mongodb_connection_string"

------------------------------------------------------------------------

## ⚙️ Local Development

Clone repo:

    git clone https://github.com/yourusername/MyConnections.git
    cd MyConnections

Install dependencies:

    pip install -r requirements.txt

Run app:

    streamlit run app.py

------------------------------------------------------------------------

## 📊 Analytics Provided

-   Total students joined\
-   Signup growth chart\
-   Recently joined list

------------------------------------------------------------------------

## 👨‍💻 Creator

## 👨‍💻 Creator

**VishnuVarDhan**

[![LinkedIn](https://img.shields.io/badge/Connect%20on-LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vishnuvardhan028/)


Built to make student networking easier.

------------------------------------------------------------------------

## 📜 License

MIT License
