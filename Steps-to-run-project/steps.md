# 🚀 Deployment Guide: Frontend on Vercel & Backend on Render

Follow these steps to deploy your full-stack application.

---

## 1. Preparation
Before starting, push your entire project to a **GitHub repository**. 
- Ensure your structure has `backend/` and `frontend/` folders at the root.
- Ensure `backend/requirements.txt` is up-to-date.
- Ensure `frontend/package.json` has the correct scripts.

---

## 2. Deploy Backend on Render
1. **Sign in** to [Render](https://render.com/).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Set the following configurations:
   - **Name**: `prediction-backend` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Go to the **Environment** tab and add:
   - `ALLOWED_ORIGINS`: `*` (or your Vercel URL once deployed for better security).
6. Click **Create Web Service**. 
7. Once deployed, copy your Render URL (e.g., `https://prediction-backend.onrender.com`).

---

## 3. Deploy Frontend on Vercel
1. **Sign in** to [Vercel](https://vercel.com/).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Set the following configurations:
   - **Project Name**: `prediction-frontend`
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
5. Open **Environment Variables** and add:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-backend-url.onrender.com` (use the URL from Step 2).
6. Click **Deploy**.
7. Once finished, copy your Vercel URL (e.g., `https://prediction-frontend.vercel.app`).

---

## 4. Final Connection (Recommended for Security)
To restrict backend access to only your frontend:
1. Go back to your **Render** dashboard.
2. Open your backend service > **Environment**.
3. Update `ALLOWED_ORIGINS` to your Vercel URL:
   - `ALLOWED_ORIGINS`: `https://prediction-frontend.vercel.app`
4. Render will automatically redeploy with the new settings.

---

## 5. Summary of Environment Variables

| Service | Environment Variable | Value |
|---------|----------------------|-------|
| **Backend (Render)** | `ALLOWED_ORIGINS` | `<your-vercel-domain>` |
| **Frontend (Vercel)** | `NEXT_PUBLIC_API_URL` | `<your-render-domain>` |

---

✅ **Your application should now be live!**
- Access the frontend at your Vercel URL.
- The frontend will communicate with the backend on Render for predictions.
