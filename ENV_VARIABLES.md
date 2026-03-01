# Environment Variables Reference

## Required Environment Variables for Vercel Deployment

Copy these environment variables to your Vercel project settings:

### Database Configuration
```
DATABASE_URL=postgresql+asyncpg://postgres:lvJetgjuE878z1r9@db.qneuianspdpxfitqgbwc.supabase.co:5432/postgres
DATABASE_ECHO=false
```

### Security Configuration
```
SECRET_KEY=your-secure-random-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Server Configuration
```
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### Logging Configuration
```
LOG_LEVEL=INFO
```

### CORS Configuration (Update with your domains)
```
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

### Optional Redis Configuration (Keep disabled if not using)
```
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379
```

## How to Generate SECRET_KEY

Run this command in your terminal:
```bash
openssl rand -hex 32
```

Example output:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

Use this value for the `SECRET_KEY` environment variable.

## Variable Descriptions

| Variable | Purpose | Example | Required |
|----------|---------|---------|----------|
| `DATABASE_URL` | Supabase PostgreSQL connection string | `postgresql+asyncpg://...` | ✅ Yes |
| `DATABASE_ECHO` | Enable SQL query logging | `false` | ✅ Yes |
| `SECRET_KEY` | JWT signing secret | 32+ character random string | ✅ Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | ✅ Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `30` | ✅ Yes |
| `HOST` | Server bind address | `0.0.0.0` | ✅ Yes |
| `PORT` | Server port (overridden by Vercel) | `8000` | ✅ Yes |
| `DEBUG` | Enable debug mode | `false` | ✅ Yes |
| `LOG_LEVEL` | Logging level | `INFO` | ✅ Yes |
| `CORS_ORIGINS` | Allowed origins for CORS | JSON array of URLs | ✅ Yes |
| `REDIS_ENABLED` | Enable Redis caching | `false` | ❌ No |
| `REDIS_URL` | Redis connection string | `redis://...` | ❌ No |

## Environment-Specific Values

### Production (Vercel)
```
DEBUG=false
LOG_LEVEL=INFO
DATABASE_ECHO=false
CORS_ORIGINS=["https://yourdomain.com"]
```

### Development (Local)
```
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_ECHO=true
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## Vercel Setup Steps

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add each variable from the table above
4. For each variable:
   - Enter the **Name** (e.g., `DATABASE_URL`)
   - Enter the **Value** (e.g., your actual connection string)
   - Select **Production** in the dropdown
   - Click **Add**
5. Deploy or redeploy your project

## Security Notes

⚠️ **IMPORTANT**: 
- Never commit your `.env` file (already in `.gitignore`)
- Use strong, random `SECRET_KEY` values
- Don't share database credentials in code
- Rotate credentials periodically
- Keep Vercel environment variables confidential
- Use HTTPS-only URLs in `CORS_ORIGINS`

## Testing Locally

Create a `.env` file in your project root with development values:
```
HOST=0.0.0.0
PORT=8000
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:lvJetgjuE878z1r9@db.qneuianspdpxfitqgbwc.supabase.co:5432/postgres
DATABASE_ECHO=true
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_ENABLED=false
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

Then run:
```bash
source venv/bin/activate
uvicorn src.main:app --reload
```

## Vercel API URL

After deployment, your API will be available at:
```
https://your-project-name.vercel.app
```

Test it:
```bash
# Health check
curl https://your-project-name.vercel.app/health

# Get contacts
curl https://your-project-name.vercel.app/api/v1/contacts

# View API docs
https://your-project-name.vercel.app/api/docs
```

---

**Need help?** Check `VERCEL_DEPLOYMENT.md` for complete deployment instructions.
