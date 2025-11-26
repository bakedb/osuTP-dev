# Tournament Registration System Guide

## Overview
The registration system allows users to register for the osu! tournament directly from the website. Registration data is collected via a form and submitted to Google Sheets for tournament organizers to review.

## Features
- **Registration Form**: Complete tournament registration with validation
- **Google Sheets Integration**: Automatic data collection (with localStorage fallback)
- **Form Validation**: Client-side validation for all required fields
- **Responsive Design**: Works on desktop and mobile devices
- **Theme Support**: Matches the existing website theme (dark and Frutiger Aero)

## Registration Fields
1. **Username** - Required field for user identification
2. **Email** - Required field with email format validation
3. **osu! Username** - Required field for player identification
4. **osu! User ID** - Required numeric field for unique identification
5. **Country** - Required field for regional grouping
6. **Preferred Difficulty Bracket** - Required dropdown selection
7. **Experience Level** - Required dropdown selection
8. **Additional Comments** - Optional textarea for extra information

## Data Storage
### Primary Method: Google Sheets
- Registration data is sent to Google Sheets (Tab 4/gid=3)
- Uses the same Google Sheets ID as other tournament data
- Requires Google Apps Script Web App for direct writing

### Fallback Method: Local Storage
- If Google Sheets integration fails, data is stored in browser localStorage
- Data can be retrieved via browser console or exported
- Key: `tournamentRegistrations`

## Google Sheets Setup
To enable direct Google Sheets writing:

1. **Create Google Apps Script Web App**:
   - Open your Google Sheet
   - Go to Extensions > Apps Script
   - Create a script to handle POST requests
   - Deploy as Web App with appropriate permissions

2. **Update the JavaScript**:
   - Replace the localStorage fallback with the Web App URL
   - Uncomment and modify the fetch request in `submitRegistrationToGoogleSheets()`

## Sample Google Apps Script
```javascript
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Registrations");
    
    // Add new row with registration data
    sheet.appendRow([
      data.username,
      data.email,
      data.osuUsername,
      data.osuId,
      data.country,
      data.preferredBracket,
      data.experience,
      data.comments,
      data.timestamp
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({success: true}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({success: false, error: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

## Styling
The registration form inherits all styling from the existing theme system:
- Dark theme support
- Frutiger Aero theme support
- Responsive modal design
- Consistent button and input styling

## Validation Rules
- All required fields must be filled
- Email must be valid format
- osu! User ID must be a positive number
- Dropdown selections must be made

## User Experience
- Modal popup for registration
- Clear error messages
- Success confirmation
- Keyboard navigation support (Enter to submit)
- Click outside to close

## Troubleshooting
1. **Registration not saving**: Check browser localStorage for fallback data
2. **Google Sheets not updating**: Ensure Web App is properly deployed
3. **Validation errors**: Check console for detailed error messages
4. **Theme issues**: Verify CSS classes are properly applied

## Future Enhancements
- Email verification
- Duplicate registration prevention
- Registration status tracking
- Export functionality for organizers
- Integration with osu! API for profile verification
