# Registration Code System Guide

## Overview
Instead of submitting registration data to external services, this system generates short, encoded codes that tournament organizers can decode to view complete registration information.

## How It Works

### For Participants
1. **Fill out the registration form** - Complete all required fields
2. **Receive your code** - After submission, you'll get a code like: `REG-XXXXXXXXXXXX-1234`
3. **Save the code** - Take a screenshot or copy the code
4. **Provide to organizers** - Share this code with tournament staff

### For Organizers
1. **Access the Tools section** - Sign in as Admin/Participant
2. **Open Registration Decoder** - Click "Show Registration Decoder"
3. **Enter the code** - Input the participant's registration code
4. **View registration details** - See all submitted information instantly

## Code Format
```
REG-[ENCODED_DATA]-[CHECKSUM]
```

- **REG**: Prefix identifying it as a registration code
- **ENCODED_DATA**: Base64-encoded registration information (12 characters)
- **CHECKSUM**: 4-character hexadecimal checksum for validation

## Features

### Security
- **Checksum validation**: Prevents tampering with codes
- **Local storage**: Data stored only in browser localStorage
- **No external dependencies**: Works completely offline

### Convenience
- **Short codes**: Easy to copy and share
- **Instant decoding**: No waiting for external services
- **Print functionality**: Generate printable registration records
- **Copy to clipboard**: Quick code sharing

### Reliability
- **Backup storage**: Registrations also saved in general localStorage
- **Error handling**: Clear error messages for invalid codes
- **Data integrity**: Checksum ensures data hasn't been corrupted

## Admin Panel Features

### Registration Decoder
- **Code validation**: Checks format and checksum
- **Data display**: Shows all registration fields in organized layout
- **Copy code**: Quick clipboard copying
- **Print registration**: Generate printable records
- **Error messages**: Helpful feedback for invalid codes

### Displayed Information
- Username and email
- Country and preferred bracket
- Experience level
- osu! account details (if provided)
- Registration timestamp
- Additional comments
- Original registration code

## Technical Details

### Code Generation Process
1. **Create registration object** with all form data
2. **Generate checksum** from data string
3. **Base64 encode** the registration data
4. **Create final code** with format `REG-[encoded]-[checksum]`
5. **Store data** in localStorage with code as key

### Decoding Process
1. **Validate code format** using regex pattern
2. **Retrieve stored data** from localStorage using code
3. **Verify checksum** to ensure data integrity
4. **Display formatted information** in admin panel

### Storage
- **Individual registrations**: `localStorage.setItem('reg_[CODE]', JSON.stringify(data))`
- **Backup storage**: `localStorage.setItem('tournamentRegistrations', JSON.stringify(allRegistrations))`

## Usage Examples

### Participant Registration
```
1. Click "Register" button
2. Fill out all fields
3. Click "Register"
4. See success message: "Registration successful! Your registration code is: REG-ABC123XYZ789-F4E2"
5. Save the code
```

### Admin Decoding
```
1. Sign in as Admin
2. Go to Tools tab
3. Click "Show Registration Decoder"
4. Enter: REG-ABC123XYZ789-F4E2
5. Click "Decode Registration"
6. View complete registration details
```

## Troubleshooting

### Common Issues
- **Invalid code format**: Ensure code starts with "REG-" and has correct structure
- **Code not found**: Registration data may have been cleared from localStorage
- **Checksum failed**: Code may have been corrupted or modified

### Solutions
- **Double-check code**: Verify exact code from participant
- **Clear cache**: If localStorage is full, clear old registrations
- **Backup codes**: Export registrations regularly to prevent data loss

## Advantages Over External Services

### Privacy
- **No third-party services**: Data never leaves the browser
- **Local control**: Complete control over registration data
- **No API limits**: Unlimited registrations without restrictions

### Simplicity
- **No setup required**: Works immediately without configuration
- **No maintenance**: No servers or databases to maintain
- **No costs**: Completely free to use

### Reliability
- **Offline capable**: Works without internet connection
- **Instant processing**: No waiting for external responses
- **No downtime**: Always available when needed

## Best Practices

### For Organizers
- **Regular backups**: Export registration data periodically
- **Code verification**: Always verify codes with participants
- **Data security**: Clear localStorage after tournament completion

### For Participants
- **Save codes immediately**: Don't rely on browser storage
- **Double-check information**: Review data before submission
- **Keep backup**: Store code in multiple safe locations

## Future Enhancements

Potential improvements could include:
- **Export functionality**: Download registrations as CSV/JSON
- **Search functionality**: Find registrations by username/email
- **Bulk operations**: Process multiple codes at once
- **Statistics**: Registration analytics and reporting
- **Email integration**: Send codes via email automatically

This system provides a secure, simple, and reliable way to handle tournament registrations without requiring external services or complex infrastructure.
