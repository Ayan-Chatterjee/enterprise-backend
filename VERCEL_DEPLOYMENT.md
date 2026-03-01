# Vercel Deployment Guide for FastAPI Backend

## ⚙️ Environment Variables to Set in Vercel

Add these environment variables in your Vercel project settings:

| Variable | Value | Example |
|----------|-------|---------|
| `HOST` | `0.0.0.0` | Required for Vercel |
| `PORT` | `8000` | Default port (Vercel overrides this) |
| `DEBUG` | `false` | Set to `false` in production |
| `DATABASE_URL` | Your Supabase PostgreSQL connection string | `postgresql+asyncpg://postgres:YOUR_PASSWORD@db.qneuianspdpxfitqgbwc.supabase.co:5432/postgres` |
| `DATABASE_ECHO` | `false` | Disable SQL logging in production |
| `SECRET_KEY` | A strong random secret | Generate a random 32+ character string |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `REDIS_URL` | `redis://...` (optional) | Only if using Redis |
| `REDIS_ENABLED` | `false` | Keep disabled unless needed |
| `LOG_LEVEL` | `INFO` | Production log level |
| `CORS_ORIGINS` | JSON array of allowed origins | `["https://yourdomain.com","https://www.yourdomain.com"]` |

## 🚀 Step-by-Step Deployment Instructions

### Step 1: Prepare Your Code
Your code is ready! The `vercel.json` and `.vercelignore` files have been created.

### Step 2: Connect GitHub to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Sign in or create an account
3. Click **"Add New"** → **"Project"**
4. Import your GitHub repository: `Ayan-Chatterjee/enterprise-backend`
5. Select the repository and click **"Import"**

### Step 3: Configure Environment Variables

In the Vercel project settings:

1. Go to **Settings** → **Environment Variables**
2. Add each variable from the table above:

```
HOST = 0.0.0.0
PORT = 8000
DEBUG = false
DATABASE_URL = postgresql+asyncpg://postgres:lvJetgjuE878z1r9@db.qneuianspdpxfitqgbwc.supabase.co:5432/postgres
DATABASE_ECHO = false
SECRET_KEY = your-very-secure-secret-key-min-32-characters-long-change-this
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REDIS_ENABLED = false
LOG_LEVEL = INFO
CORS_ORIGINS = ["https://yourdomain.com","https://www.yourdomain.com"]
```

⚠️ **IMPORTANT**: 
- Replace `SECRET_KEY` with a strong, random secret (use `openssl rand -hex 32`)
- Update `CORS_ORIGINS` with your actual frontend domains
- Keep `DATABASE_URL` secure (don't share it publicly)

### Step 4: Generate Secure SECRET_KEY

Run this in your terminal to generate a secure secret:
```bash
openssl rand -hex 32
```

Copy the output and paste it into the `SECRET_KEY` environment variable in Vercel.

### Step 5: Deploy

1. Click **"Deploy"** button in Vercel
2. Wait for the deployment to complete (usually 1-2 minutes)
3. Your API will be live at: `https://your-project-name.vercel.app`

### Step 6: Test Your Deployment

Once deployed, test your API:

```bash
# Get all contacts
curl https://your-project-name.vercel.app/api/v1/contacts

# Access Swagger documentation
https://your-project-name.vercel.app/api/docs
```

## 🔗 Database Connection

Your Supabase PostgreSQL database is already configured:
- **Host**: db.qneuianspdpxfitqgbwc.supabase.co
- **Port**: 5432
- **Database**: postgres
- **User**: postgres
- **Connection String**: Set via `DATABASE_URL` environment variable

## 🔒 Security Best Practices

1. **Never commit `.env`** - Already in `.gitignore`
2. **Use strong SECRET_KEY** - Generate with `openssl rand -hex 32`
3. **Rotate credentials** - Change database password periodically
4. **Use environment variables** - All sensitive data should be in Vercel settings
5. **CORS Origins** - Only allow trusted domains in `CORS_ORIGINS`
6. **HTTPS** - Vercel provides free HTTPS for all deployments

## 📊 Environment Variables by Environment

### Development (Local)
```
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### Production (Vercel)
```
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🛠️ Vercel Configuration Details

The `vercel.json` file configuration:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.13"
  }
}
```

This tells Vercel to:
- Use Python 3.13
- Build and run `src/main.py` with Gunicorn
- Route all requests to the FastAPI app

## 🚨 Common Issues & Solutions

### Issue: Database connection timeout
**Solution**: Ensure your Supabase IP whitelist includes Vercel's IP range (0.0.0.0/0)

### Issue: Secret key not working
**Solution**: Regenerate SECRET_KEY using `openssl rand -hex 32` and update in Vercel

### Issue: CORS errors
**Solution**: Add your Vercel domain to `CORS_ORIGINS` in environment variables

### Issue: 502 Bad Gateway
**Solution**: Check Vercel logs - likely a configuration issue with environment variables

## 📝 API Endpoints Available

Once deployed, all these endpoints are live:

```
GET  /health                          # Health check
GET  /api/v1/contacts                 # List contacts
POST /api/v1/contacts                 # Create contact
GET  /api/v1/contacts/{id}            # Get contact
GET  /api/v1/callbacks                # List callbacks
POST /api/v1/callbacks                # Create callback
POST /api/v1/auth/login               # User login
GET  /api/docs                        # Swagger documentation
GET  /api/redoc                       # ReDoc documentation
```

## 🔍 Monitoring & Logs

Check your Vercel deployment logs:
1. Go to your Vercel project dashboard
2. Click on a deployment
3. View logs in the **Logs** tab

## 🎯 Next Steps

1. ✅ Create vercel.json (done)
2. ✅ Create .vercelignore (done)
3. ⏭️ Push changes to GitHub
4. ⏭️ Connect repository to Vercel
5. ⏭️ Set environment variables
6. ⏭️ Deploy
7. ⏭️ Test your API

## 📞 Support

For Vercel-specific issues:
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/docs/concepts/functions/serverless-functions)

---

**Your backend is ready for Vercel deployment!** 🚀
