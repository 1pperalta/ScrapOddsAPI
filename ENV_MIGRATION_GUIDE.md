# 🔧 Environment Variables Migration Guide

## 📊 **Current Situation (Before)**

You have multiple `.env` files:
```
❌ scrapping/.env
❌ odds-agent/backend/server_py/.env
```

**Problems:**
- Duplicate keys across files
- Hard to maintain
- Easy to get out of sync
- Violates DRY principle

---

## ✅ **New Structure (After)**

Single `.env` file at project root:
```
✅ ScrapOddsAPI/.env  (single source of truth)
✅ ScrapOddsAPI/.env.example  (template for team)
```

**Benefits:**
- Single source of truth
- Easy to maintain
- No duplication
- Team members can copy `.env.example`

---

## 🚀 **Migration Steps**

### **Step 1: Create Root `.env` File**

```bash
cd "/Users/1pperalta/Documents/pablo cosas /UPB/PATIC/ScrapOddsAPI"

# Copy the example
cp .env.example .env

# Or if you already have a .env in scrapping/, move it:
# mv scrapping/.env .env
```

### **Step 2: Edit the Root `.env` File**

Open `ScrapOddsAPI/.env` and add your actual keys:

```bash
# ---- API Keys ----
ODDS_API_KEY=your_actual_odds_api_key
GOOGLE_API_KEY=your_actual_gemini_key

# ---- Database Configuration ----
DB_HOST=localhost
DB_PORT=5432
DB_NAME=betting_odds
DB_USER=postgres
DB_PASSWORD=oddsupb
```

### **Step 3: Delete Old `.env` Files**

```bash
# Remove the old individual .env files
rm -f scrapping/.env
rm -f odds-agent/backend/server_py/.env
```

### **Step 4: Test Everything**

**Test 1: Database**
```bash
docker-compose up -d
docker ps | grep betting_odds_db
```

**Test 2: Scrapper**
```bash
cd scrapping
python scrapping.py
# Should find root .env ✅
```

**Test 3: Backend**
```bash
cd odds-agent/backend/server_py
python3 app.py
# Should find root .env ✅
```

**Test 4: Frontend**
```bash
cd odds-agent/frontend
npm run dev
# Should work ✅
```

---

## 🔍 **How It Works Now**

### **Scrapper (`scrapping.py`)**
```python
# Now loads from project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(project_root, '.env'))
```

**Path resolution:**
- Script location: `ScrapOddsAPI/scrapping/scrapping.py`
- Goes up one level: `ScrapOddsAPI/`
- Loads: `ScrapOddsAPI/.env` ✅

### **Backend Agent (`agent.py`)**
```python
# Automatically searches up the directory tree
load_dotenv()
```

**Path resolution:**
- Script location: `ScrapOddsAPI/odds-agent/backend/server_py/agent.py`
- `load_dotenv()` searches: `server_py/`, `backend/`, `odds-agent/`, `ScrapOddsAPI/`
- Finds: `ScrapOddsAPI/.env` ✅

---

## 📁 **New Project Structure**

```
ScrapOddsAPI/
├── .env                    ← 🆕 Single source of truth!
├── .env.example           ← 🆕 Template for team
├── .gitignore             ← Already ignores .env
├── docker-compose.yml
├── README.md
│
├── scrapping/
│   ├── scrapping.py       ← ✅ Updated to use root .env
│   └── requirements.txt
│
└── odds-agent/
    └── backend/
        └── server_py/
            ├── app.py
            ├── agent.py   ← ✅ Already uses root .env
            └── requirements.txt
```

---

## 🛡️ **Security Notes**

### **✅ What's Protected**

Your `.gitignore` already has:
```gitignore
# Environment files (NEVER commit API keys!)
.env
.env.local
.env.*.local
scrapping/.env
odds-agent/backend/server_py/.env
```

### **✅ What to Commit**

- ✅ `.env.example` (template without secrets)
- ❌ `.env` (contains your actual API keys)

### **✅ For Team Members**

When someone clones the repo:
```bash
# 1. Copy the template
cp .env.example .env

# 2. Add their own API keys
nano .env  # or use any editor

# 3. Start working!
```

---

## 🧪 **Verification Checklist**

After migration, verify:

- [ ] Root `.env` file exists with all keys
- [ ] `scrapping/.env` deleted
- [ ] `odds-agent/backend/server_py/.env` deleted
- [ ] Scrapper runs successfully
- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] `.env.example` is committed to Git
- [ ] `.env` is NOT committed to Git

---

## 🆘 **Troubleshooting**

### **"ModuleNotFoundError: No module named 'google.generativeai'"**

```bash
cd odds-agent/backend/server_py
pip3 install -r requirements.txt
```

### **"API_KEY not found"**

Check that root `.env` has the key:
```bash
cat .env | grep API_KEY
```

### **"Database connection failed"**

Check database credentials in root `.env`:
```bash
cat .env | grep DB_
```

And verify Docker is running:
```bash
docker ps | grep betting_odds_db
```

---

## 🎯 **Summary**

**Before:**
```
scrapping/.env              (Keys + DB config)
odds-agent/.../server_py/.env  (Keys + DB config)
❌ Duplication! Hard to maintain!
```

**After:**
```
.env                        (Keys + DB config)
.env.example               (Template)
✅ Single source of truth!
```

**Commands:**
```bash
# 1. Create root .env from your current scrapping/.env
mv scrapping/.env .env

# 2. Delete the duplicate
rm odds-agent/backend/server_py/.env

# 3. Test everything works
docker-compose up -d
cd scrapping && python scrapping.py
cd ../odds-agent/backend/server_py && python3 app.py
```

---

**✅ Migration Complete!** Your environment variables are now centralized and easy to manage.

