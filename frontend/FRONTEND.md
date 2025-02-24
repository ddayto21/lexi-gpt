## View Network Request Logs

```bash
grc tail -f dev.log | bat --language=log --paging=never
```

## Testing for Deployment

### Step 1: Build and Serve the App Locally

Ensure you have already installed the `serve` package:

```bash
yarn global serve
```

Before deploying new changes to the codebase, we will test how the app performs in in production mode by running the following commands:

```bash
yarn build
```

- This generates an optimized build/ folder (minified, tree-shaken).

Then, we can serve the build locally by running the application as if it were deployed with the following command:

```bash
npx serve -s build
```

- This command will detect missing environment variables or API issuess.

### Step 2: Run Tests

Ensure core logic and UI compoennts work correctly:

```bash
yarn test
```

Run API and component integration tests:

```bash
yarn test:integration
```

Simulate real user interactions across the app:

```bash
yarn test:e2e
```

## Environment Variables

Dynamically configuring environment variables for development, CI/CD environment, and production.

- Current problem: the react application is currently hardcoded to proxy api requests to "http://localhost:8000", which will not work in production.

- Frontend must detect which environment it is running in (development) or on AWS (production) and set the environment variables accordingly.

### Mixed Content Block

HTTPS frontend sending api requets to HTTP.

Current problem: the react application is served over HTTPS, but the API behind AWS ECS is served over HTTP.

- Modern browsers typically block "Mixed Content" requests (secure-to-insecure communication) for security reasons.


