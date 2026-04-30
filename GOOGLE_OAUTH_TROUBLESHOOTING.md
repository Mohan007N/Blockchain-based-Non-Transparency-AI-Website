# Google OAuth Troubleshooting Guide

## Issue: "window is not defined" Error

### Problem
When clicking "Continue with Google", you see an error: "window is not defined"

### Cause
The error occurs because TanStack Router tries to access `window` object during server-side rendering (SSR), but `window` is only available in the browser.

### Solution ✅
**FIXED** - Updated `src/routes/auth.tsx` to:
1. Use `useEffect` hook instead of `beforeLoad` for handling OAuth callback
2. Check `typeof window !== 'undefined'` before accessing window object
3. Added loading state during Google OAuth process

### Code Changes Applied

```typescript
// Before (WRONG - causes SSR error)
export const Route = createFileRoute("/auth")({
  component: AuthPage,
  beforeLoad: ({ search }) => {
    const urlParams = new URLSearchParams(window.location.search); // ❌ Error!
    // ...
  }
});

// After (CORRECT - works with SSR)
export const Route = createFileRoute("/auth")({
  component: AuthPage,
});

function AuthPage() {
  useEffect(() => {
    if (typeof window !== 'undefined') { // ✅ Check if browser
      const urlParams = new URLSearchParams(window.location.search);
      // Handle OAuth callback
    }
  }, []);
}
```

## Current Flow

### Step 1: User Clicks "Continue with Google"
- Button shows loading state
- Redirects to: `http://localhost:5000/api/auth/google`

### Step 2: Backend Redirects to Google
- Backend generates OAuth URL
- User sees Google consent screen

### Step 3: User Authorizes
- Google redirects to: `http://localhost:5000/api/auth/google/callback?code=...`

### Step 4: Backend Processes
- Exchanges code for access token
- Fetches user info from Google
- Creates/updates user in database
- Generates JWT token
- Redirects to: `http://localhost:8080/auth?token=...&user=...`

### Step 5: Frontend Completes Login
- `useEffect` detects token in URL
- Shows "Completing Google Sign In..." loading screen
- Fetches user details from `/api/auth/me`
- Stores token and user in localStorage
- Redirects to dashboard
- Shows success toast

## Testing Steps

1. **Clear browser data** (to test fresh login):
   ```
   - Open DevTools (F12)
   - Application tab → Storage → Clear site data
   ```

2. **Navigate to auth page**:
   ```
   http://localhost:8080/auth
   ```

3. **Click "Continue with Google"**:
   - Should show loading spinner
   - Should redirect to Google

4. **Authorize the app**:
   - Select your Google account
   - Click "Continue" or "Allow"

5. **Verify redirect**:
   - Should see "Completing Google Sign In..." screen
   - Should redirect to dashboard
   - Should see success toast

## Common Issues

### Issue 1: Redirect URI Mismatch
**Error**: `redirect_uri_mismatch`

**Solution**: Add these URLs in Google Cloud Console:
```
http://localhost:5000/api/auth/google/callback
http://localhost:8080/auth
```

### Issue 2: Invalid Client
**Error**: `invalid_client`

**Solution**: Verify credentials in `.env`:
```env
GOOGLE_CLIENT_ID=608687632539-2o6insdcvhdb2i1bvq6k6mcqart8rfq3.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```

### Issue 3: CORS Error
**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**: Backend already configured with CORS. Check `.env`:
```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8080
```

### Issue 4: Token Not Stored
**Error**: User redirected but not logged in

**Solution**: 
1. Check browser console for errors
2. Verify localStorage is enabled
3. Check network tab for `/api/auth/me` response

### Issue 5: Infinite Redirect Loop
**Error**: Page keeps redirecting

**Solution**:
1. Clear browser localStorage
2. Clear URL parameters
3. Restart both services

## Debug Checklist

- [ ] Both services running (backend on 5000, frontend on 8080)
- [ ] Google credentials in `.env` are correct
- [ ] Redirect URIs added in Google Cloud Console
- [ ] Browser localStorage is enabled
- [ ] No browser extensions blocking redirects
- [ ] Network tab shows successful API calls
- [ ] Console shows no JavaScript errors

## Backend Logs

### Successful Flow
```
INFO: GET /api/auth/google HTTP/1.1" 307 Temporary Redirect
INFO: GET /api/auth/google/callback?code=... HTTP/1.1" 307 Temporary Redirect
INFO: Google OAuth login: user@example.com
INFO: GET /api/auth/me HTTP/1.1" 200 OK
```

### Failed Flow
```
ERROR: Failed to exchange code for token
ERROR: Google OAuth error: ...
```

## Frontend Console

### Successful Flow
```
✓ Google login successful!
✓ Navigating to /dashboard
```

### Failed Flow
```
✗ Failed to fetch user details
✗ Failed to complete login
```

## Quick Fix Commands

### Restart Backend
```bash
cd ai-service
python main_with_auth.py
```

### Restart Frontend
```bash
cd verity-ai-main
npm run dev
```

### Clear Browser Data
```javascript
// Run in browser console
localStorage.clear();
sessionStorage.clear();
location.reload();
```

## Status

✅ **FIXED** - Window is not defined error resolved
✅ **WORKING** - Google OAuth flow functional
✅ **TESTED** - Successfully tested with Google account

## Support

If issues persist:
1. Check backend logs for detailed errors
2. Check browser console for JavaScript errors
3. Verify all redirect URIs in Google Cloud Console
4. Ensure both services are running
5. Try with a different browser

---

**Last Updated**: 2026-04-29
**Status**: Working
