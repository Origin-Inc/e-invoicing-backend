# Environment Variables Configuration

This document describes how to configure environment variables for the E-Invoicing frontend application.

## Quick Setup

1. Copy the example file:
   ```bash
   cp .env.example .env.local
   ```

2. Update the values in `.env.local` for your environment

## Environment Files

- `.env.local` - Local development overrides (gitignored)
- `.env.example` - Template with all available variables
- `.env.development` - Development defaults (if needed)
- `.env.production` - Production overrides (if needed)

## Available Variables

### Required Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://127.0.0.1:8002` | `https://api.myapp.com` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `E-Invoicing System` | `My Invoice App` |
| `NEXT_PUBLIC_APP_VERSION` | Application version | `0.1.0` | `1.2.3` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `NEXT_PUBLIC_APP_ENV` | Environment name | `development` | `production` |
| `NEXT_PUBLIC_DEBUG` | Enable debug mode | `false` | `true` |
| `NEXT_PUBLIC_LOG_LEVEL` | Logging level | `info` | `debug` |

## Usage in Code

```typescript
import { API_BASE_URL, APP_NAME, DEBUG_MODE } from '@/lib/constants';
import { getEnvironmentConfig, validateEnvironment } from '@/lib/utils';

// Direct usage
const apiUrl = API_BASE_URL;

// Get all config at once
const config = getEnvironmentConfig();

// Validate environment
const { isValid, errors } = validateEnvironment();
if (!isValid) {
  console.error('Environment validation failed:', errors);
}
```

## Environment Validation

The application includes built-in environment validation:

- Checks all required variables are present
- Validates URL formats
- Provides helpful error messages
- Safe logging in development mode

## Security Notes

1. **Client-side Variables**: All `NEXT_PUBLIC_*` variables are bundled into the client-side code
2. **Sensitive Data**: Never put secrets in `NEXT_PUBLIC_*` variables
3. **Production**: Use proper secrets management for production deployments
4. **Git**: `.env.local` is automatically gitignored

## Development vs Production

### Development
- Uses `.env.local` for local overrides
- Debug mode enabled by default
- API points to local backend (port 8002)

### Production
- Environment variables from deployment platform
- Debug mode disabled
- API points to production backend
- Optimized builds with environment variable injection

## Troubleshooting

### Variables Not Loading
1. Check file naming (`.env.local`, not `.env.local.txt`)
2. Ensure `NEXT_PUBLIC_` prefix for client-side variables
3. Restart development server after changes
4. Check for syntax errors (no spaces around `=`)

### Build Errors
1. Run environment validation: `validateEnvironment()`
2. Check all required variables are set
3. Verify URL formats are valid

### API Connection Issues
1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check backend is running on specified port
3. Ensure no CORS issues between frontend/backend 