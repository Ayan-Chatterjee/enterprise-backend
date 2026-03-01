# Vercel Deployment Checklist ✅

## Pre-Deployment Setup

- [x] Code pushed to GitHub: https://github.com/Ayan-Chatterjee/enterprise-backend
- [x] `vercel.json` configuration created
- [x] `.vercelignore` created
- [x] `.env` is in `.gitignore` (secure)
- [x] Environment variables documentation created

## Step-by-Step Deployment

### 1️⃣ Connect Repository to Vercel
- [ ] Go to https://vercel.com
- [ ] Sign in with GitHub account
- [ ] Click **"Add New"** → **"Project"**
- [ ] Search for and select: `enterprise-backend`
- [ ] Click **"Import"**

### 2️⃣ Configure Project Settings
- [ ] Go to **Settings** tab
- [ ] Set **Framework Preset** to `Other`
- [ ] Set **Build Command** to: (leave empty - Vercel auto-detects)
- [ ] Set **Output Directory** to: (leave empty)

### 3️⃣ Add Environment Variables

Go to **Settings** → **Environment Variables** and add:

#### Required Variables
- [ ] `HOST` = `0.0.0.0`
- [ ] `PORT` = `8000`
- [ ] `DEBUG` = `false`
- [ ] `DATABASE_URL` = `postgresql+asyncpg://postgres:lvJetgjuE878z1r9@db.qneuianspdpxfitqgbwc.supabase.co:5432/postgres`
- [ ] `DATABASE_ECHO` = `false`
- [ ] `SECRET_KEY` = (generate with: `openssl rand -hex 32`)
- [ ] `ALGORITHM` = `HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
- [ ] `LOG_LEVEL` = `INFO`
- [ ] `CORS_ORIGINS` = `["https://yourdomain.com"]` (update with your domain)

#### Optional Variables
- [ ] `REDIS_ENABLED` = `false` (only if using Redis)
- [ ] `REDIS_URL` = (only if using Redis)

### 4️⃣ Generate SECRET_KEY
Run in your terminal:
```bash
openssl rand -hex 32
```
Copy the output (e.g., `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`) and paste into `SECRET_KEY` in Vercel.

### 5️⃣ Deploy
- [ ] Go to **Deployments** tab
- [ ] Click **"Deploy"** button
- [ ] Wait for deployment to complete (1-2 minutes)

### 6️⃣ Verify Deployment
- [ ] Check Vercel shows "Ready" status
- [ ] Note your deployment URL: `https://your-project-name.vercel.app`
- [ ] Test the API:
  ```bash
  curl https://your-project-name.vercel.app/health
  ```
  Should return: `{"status":"ok","message":"Server is running"}`

## Testing Your Deployed API

### Health Check
```bash
curl https://your-project-name.vercel.app/health
```

### Get Contacts
```bash
curl https://your-project-name.vercel.app/api/v1/contacts
```

### Access API Documentation
```
https://your-project-name.vercel.app/api/docs
```

## Environment Variable Quick Reference

| Variable | Value |
|----------|-------|
| HOST | `0.0.0.0` |
| PORT | `8000` |
| DEBUG | `false` |
| DATABASE_URL | Supabase connection string |
| DATABASE_ECHO | `false` |
| SECRET_KEY | Random 32+ char string |
| ALGORITHM | `HS256` |
| ACCESS_TOKEN_EXPIRE_MINUTES | `30` |
| LOG_LEVEL | `INFO` |
| CORS_ORIGINS | `["https://yourdomain.com"]` |

## Troubleshooting

### Issue: 502 Bad Gateway
**Solution**: Check environment variables are all set correctly in Vercel Settings

### Issue: Database Connection Error
**Solution**: Verify `DATABASE_URL` is correct and Supabase allows Vercel IP

### Issue: CORS Errors
**Solution**: Update `CORS_ORIGINS` to include your frontend domain

### Issue: Logs show errors
**Solution**: Go to Deployments → [Latest] → Logs tab to see detailed error messages

## Security Reminders

✅ **Do**:
- Generate strong `SECRET_KEY` with `openssl rand -hex 32`
- Use environment variables in Vercel, not in code
- Keep `.env` file local only (in `.gitignore`)
- Use HTTPS URLs in `CORS_ORIGINS`
- Rotate credentials periodically

❌ **Don't**:
- Commit `.env` to GitHub
- Share database credentials
- Use weak secret keys
- Enable DEBUG in production
- Allow `*` in CORS_ORIGINS without justification

## After Deployment

1. **Update your frontend** to use the new API URL: `https://your-project-name.vercel.app`

2. **Monitor logs** regularly:
   - Vercel Dashboard → Your Project → Logs
   - Check for errors or unusual activity

3. **Test all endpoints** to ensure they work correctly

4. **Set up alerts** (optional):
   - Vercel Dashboard → Settings → Notifications
   - Get notified of deployment failures

## Next Steps

- [ ] Deploy to Vercel (follow steps above)
- [ ] Test all API endpoints
- [ ] Update frontend to use new API URL
- [ ] Monitor logs for any issues
- [ ] Set up custom domain (optional)
- [ ] Configure auto-deployments from GitHub

## Useful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Your GitHub Repo**: https://github.com/Ayan-Chatterjee/enterprise-backend
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI on Vercel**: https://vercel.com/docs/functions/serverless-functions

---

**Ready to deploy!** Follow the checklist above to get your API live on Vercel. 🚀
