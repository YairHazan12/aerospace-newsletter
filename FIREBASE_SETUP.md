# 🔥 Firebase Setup Guide

This guide shows you how to set up Firebase Firestore for the newsletter signup system.

## 📋 Prerequisites

- Google Cloud Platform account
- Firebase project created
- Service account key generated

## 🚀 Setup Steps

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter project name: `aerospace-newsletter` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click "Create project"

### 2. Enable Firestore Database

1. In your Firebase project, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location close to your users
5. Click "Done"

### 3. Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your Firebase project
3. Go to "IAM & Admin" → "Service Accounts"
4. Click "Create Service Account"
5. Enter name: `newsletter-service`
6. Click "Create and Continue"
7. Add role: "Firebase Admin SDK Administrator Service Agent"
8. Click "Done"
9. Click on the created service account
10. Go to "Keys" tab
11. Click "Add Key" → "Create new key"
12. Choose "JSON" format
13. Download the JSON file

### 4. Configure Environment Variables

Add these variables to your `.env` file:

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com/
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_CLIENT_ID=your-client-id
```

### 5. Extract Values from Service Account JSON

From your downloaded JSON file, copy these values:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",                    // → FIREBASE_PROJECT_ID
  "private_key_id": "your-private-key-id",            // → FIREBASE_PRIVATE_KEY_ID
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",  // → FIREBASE_PRIVATE_KEY
  "client_email": "your-service@...",                 // → FIREBASE_CLIENT_EMAIL
  "client_id": "your-client-id",                      // → FIREBASE_CLIENT_ID
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

## 🧪 Testing Firebase Integration

### Test Firebase Manager
```bash
python firebase_manager.py
```

### Test Factory
```bash
python email_manager_factory.py
```

### Test Full System
```bash
python test.py
```

## 🔧 Firestore Security Rules

For production, update your Firestore rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write for newsletter subscribers
    match /newsletter_subscribers/{email} {
      allow read, write: if true; // Adjust based on your security needs
    }
  }
}
```

## 📊 Firestore Data Structure

The system stores subscribers in the `newsletter_subscribers` collection:

```json
{
  "email": "user@example.com",
  "name": "User Name",
  "subscribed_at": "2024-01-01T12:00:00.000Z",
  "active": true,
  "unsubscribe_token": "abc123..."
}
```

## 🚨 Troubleshooting

### Common Issues

1. **"Firebase not initialized"**
   - Check all environment variables are set
   - Verify private key has proper newlines (`\n`)

2. **"Permission denied"**
   - Check Firestore security rules
   - Verify service account has proper permissions

3. **"Project not found"**
   - Verify FIREBASE_PROJECT_ID is correct
   - Check project exists in Firebase Console

### Debug Commands

```bash
# Check environment variables
python -c "import os; print('Project ID:', os.getenv('FIREBASE_PROJECT_ID'))"

# Test Firebase connection
python firebase_manager.py

# Check Firestore data
# Go to Firebase Console → Firestore Database
```

## 🔒 Security Best Practices

1. **Never commit service account JSON** to version control
2. **Use environment variables** for all credentials
3. **Set up proper Firestore rules** for production
4. **Rotate service account keys** regularly
5. **Use least privilege principle** for service account roles

## 📈 Monitoring

### Firebase Console
- Monitor database usage
- View authentication logs
- Check error rates

### Application Logs
- Check Python logs for Firebase errors
- Monitor subscription/unsubscription events
- Track API usage

## 🎯 Next Steps

Once Firebase is configured:

1. **Test the signup form** at http://localhost:5001
2. **Check Firestore** for new subscribers
3. **Test newsletter sending** with Firebase subscribers
4. **Deploy to production** with Firebase credentials

Your newsletter system will now use Firebase Firestore for reliable, scalable email management! 🚀
