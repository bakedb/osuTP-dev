# Google Sheets Integration Guide

## Overview
This guide explains how to set up Google Sheets integration for the tournament registration system. The system currently stores registration data in localStorage as a fallback, but can be configured to send data directly to Google Sheets.

## Current Setup

### Google Sheets Structure
Your Google Sheet should have the following tabs:
- **Tab 1 (gid=0)**: User accounts (username, password_hash, role)
- **Tab 2 (gid=1)**: Tournament brackets
- **Tab 3 (gid=2)**: Live scores
- **Tab 4 (gid=3)**: **Registrations** (new tab for registration data)

### Registration Data Columns (Tab 4)
Create these columns in the 4th tab:
1. **Username** - Registration username
2. **Email** - User's email address
3. **osu! Username** - osu! username (if provided)
4. **osu! User ID** - osu! numeric ID (if provided)
5. **Country** - User's country
6. **Preferred Bracket** - Selected difficulty bracket
7. **Experience Level** - Tournament experience
8. **Comments** - Additional information
9. **Timestamp** - Registration date/time

## Method 1: Google Apps Script (Recommended)

### Step 1: Create Google Apps Script
1. Open your Google Sheet
2. Go to **Extensions** > **Apps Script**
3. Delete any existing code and paste this:

```javascript
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Registrations");
    
    // If Registrations sheet doesn't exist, create it
    if (!sheet) {
      const newSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Registrations");
      newSheet.appendRow(["Username", "Email", "osu! Username", "osu! User ID", "Country", "Preferred Bracket", "Experience Level", "Comments", "Timestamp"]);
    }
    
    // Add new row with registration data
    const targetSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Registrations");
    targetSheet.appendRow([
      data.username || '',
      data.email || '',
      data.osuUsername || '',
      data.osuId || '',
      data.country || '',
      data.preferredBracket || '',
      data.experience || '',
      data.comments || '',
      data.timestamp || new Date().toISOString()
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({success: true}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    Logger.log(error.toString());
    return ContentService.createTextOutput(JSON.stringify({success: false, error: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput("Tournament Registration API")
    .setMimeType(ContentService.MimeType.TEXT);
}
```

### Step 2: Deploy as Web App
1. Click **Deploy** > **New deployment**
2. Choose **Web app**
3. Set these options:
   - **Description**: Tournament Registration API
   - **Execute as**: Me (your Google account)
   - **Who has access**: Anyone (for public registration)
4. Click **Deploy**
5. **Authorization required** - click **Authorize access**
6. Sign in with your Google account
7. Click **Allow** for the permissions
8. Copy the **Web app URL** (it looks like: `https://script.google.com/macros/s/.../exec`)

### Step 3: Update JavaScript
In `index.html`, find the `submitRegistrationToGoogleSheets` function and replace the localStorage fallback with:

```javascript
async function submitRegistrationToGoogleSheets(registrationData) {
  const scriptUrl = 'YOUR_WEB_APP_URL_HERE'; // Paste your Web app URL here
  
  try {
    const response = await fetch(scriptUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registrationData)
    });
    
    const result = await response.json();
    return result.success;
  } catch (error) {
    console.error('Failed to submit registration:', error);
    
    // Fallback to localStorage
    const existingRegistrations = JSON.parse(localStorage.getItem('tournamentRegistrations') || '[]');
    existingRegistrations.push(registrationData);
    localStorage.setItem('tournamentRegistrations', JSON.stringify(existingRegistrations));
    
    return false;
  }
}
```

## Method 2: CORS Proxy (Alternative)

If you can't use Google Apps Script, you can use a CORS proxy:

### Step 1: Set up CORS Proxy
Use a service like `cors-anywhere.herokuapp.com` or set up your own.

### Step 2: Update JavaScript
```javascript
async function submitRegistrationToGoogleSheets(registrationData) {
  const googleSheetsId = '1gwlmCixsyiyhzVzaXNGJaHyZwC5bbrVST24f1akTQI4';
  const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
  const targetUrl = `https://docs.google.com/spreadsheets/d/${googleSheetsId}/gviz/tq?tqx=out:json&gid=3`;
  
  try {
    const response = await fetch(proxyUrl + targetUrl);
    // Handle response...
  } catch (error) {
    // Fallback to localStorage
  }
}
```

## Method 3: Server-side Backend (Advanced)

Create a Node.js/Python backend that:
1. Receives registration data from the frontend
2. Uses Google Sheets API to write data
3. Handles authentication and rate limiting

### Example Node.js Backend
```javascript
const { google } = require('googleapis');

async function appendToGoogleSheets(data) {
  const auth = new google.auth.GoogleAuth({
    keyFile: 'service-account-key.json',
    scopes: ['https://www.googleapis.com/auth/spreadsheets']
  });
  
  const client = await auth.getClient();
  const sheets = google.sheets({ version: 'v4', auth: client });
  
  const range = 'Registrations!A:I';
  const values = [
    [data.username, data.email, data.osuUsername, data.osuId, 
     data.country, data.preferredBracket, data.experience, data.comments, data.timestamp]
  ];
  
  await sheets.spreadsheets.values.append({
    spreadsheetId: 'YOUR_SPREADSHEET_ID',
    range: range,
    valueInputOption: 'USER_ENTERED',
    resource: { values: values }
  });
}
```

## Testing Your Setup

### 1. Test Google Apps Script
1. Open your Web app URL in browser
2. You should see "Tournament Registration API"
3. Test with curl:
```bash
curl -X POST YOUR_WEB_APP_URL \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","country":"USA","preferredBracket":"normal","experience":"beginner","comments":"test"}'
```

### 2. Test Frontend
1. Open your website
2. Fill out the registration form
3. Check browser console for logs
4. Check Google Sheets for new data
5. Check localStorage for fallback data

## Troubleshooting

### Common Issues
1. **CORS errors**: Use Google Apps Script method
2. **Permission denied**: Check Google Sheet sharing settings
3. **Web app not deployed**: Complete the deployment process
4. **Data not appearing**: Check tab name and column order

### Debug Steps
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests
4. Verify Web app URL is correct
5. Check Google Apps Script logs

### Fallback Data Recovery
If Google Sheets fails, data is stored in localStorage:
```javascript
// Get all registrations
const registrations = JSON.parse(localStorage.getItem('tournamentRegistrations') || '[]');
console.log(registrations);

// Export data
const dataStr = JSON.stringify(registrations, null, 2);
const blob = new Blob([dataStr], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'registrations-backup.json';
a.click();
```

## Security Considerations

1. **Rate Limiting**: Add rate limiting to prevent spam
2. **Input Validation**: Validate all data on the backend
3. **Authentication**: Consider requiring Google sign-in
4. **Data Privacy**: Ensure compliance with data protection laws

## Maintenance

1. **Monitor**: Check Google Apps Script logs regularly
2. **Backup**: Export registration data periodically
3. **Update**: Keep Google Apps Script updated
4. **Test**: Test registration process before tournaments

This setup provides a robust registration system that works even if Google Sheets integration fails, with automatic fallback to local storage.
