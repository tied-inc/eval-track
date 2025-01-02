# TypeScript Tracer

A TypeScript implementation of the eval-track tracer for capturing function responses in TypeScript/JavaScript applications.

## Installation

### Prerequisites
- Node.js version 18 or higher
- pnpm (recommended), npm, or yarn
- [Task](https://taskfile.dev/) (optional, for development tasks)

### Install using package manager
```bash
# Using pnpm (recommended)
pnpm install @tied-inc/eval-track

# Or using npm
npm install @tied-inc/eval-track

# Or using yarn
yarn add @tied-inc/eval-track
```

### Install using Task (recommended for development)
```bash
# Install Task if not already installed
npm install -g @go-task/cli

# Install dependencies
task install-tracker
```

## Environment Setup

### Configuration

The tracer can be configured through the following environment variables:

| Variable Name      | Purpose                                          | Default Value            |
|-------------------|--------------------------------------------------|-------------------------|
| EVAL_TRACK_API_URL| Base URL for the eval-track API                  | http://localhost:8000   |
| DEBUG             | Enable debug logging (set to 'eval-track:*')     | undefined               |
| NODE_ENV          | Environment mode (development/production)         | development             |

## Basic Usage

```typescript
import { captureResponse } from '@tied-inc/eval-track';

// Basic synchronous function
function greet(name: string): { message: string } {
  return { message: `Hello, ${name}!` };
}

// Wrap the function
const wrappedGreet = captureResponse(greet);

// Use the wrapped function
const result = wrappedGreet('World');
console.log(result.message); // Output: Hello, World!

// Async function example
async function fetchData(): Promise<{ data: string }> {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();
  return { data };
}

// Wrap async function
const wrappedFetch = captureResponse(fetchData);

// Use the wrapped async function
try {
  const result = await wrappedFetch();
  console.log(result.data);
} catch (error) {
  console.error('Error:', error);
}
```

## Error Handling

The tracer uses Zod for runtime type validation and handles errors gracefully:

```typescript
import { z } from 'zod';
import { captureResponse } from '@tied-inc/eval-track';

// Define a schema for your response
const ResponseSchema = z.object({
  data: z.string(),
  timestamp: z.number(),
});

type Response = z.infer<typeof ResponseSchema>;

// Function that might throw an error
async function riskyOperation(): Promise<Response> {
  try {
    // Some risky operation
    return {
      data: 'Success',
      timestamp: Date.now(),
    };
  } catch (error) {
    throw new Error('Operation failed');
  }
}

// Wrap the function
const wrappedOperation = captureResponse(riskyOperation);

// Error handling in usage
try {
  const result = await wrappedOperation();
  console.log('Success:', result);
} catch (error) {
  console.error('Operation failed:', error);
}
```

## Advanced Usage

### Middleware Integration

```typescript
import express from 'express';
import { captureResponse } from '@tied-inc/eval-track';

const app = express();

// Create a middleware wrapper
const tracedHandler = (handler: express.RequestHandler): express.RequestHandler => {
  const wrapped = captureResponse(handler);
  return async (req, res, next) => {
    try {
      await wrapped(req, res, next);
    } catch (error) {
      next(error);
    }
  };
};

// Use in routes
app.get('/api/data', tracedHandler(async (req, res) => {
  const data = await fetchSomeData();
  res.json(data);
}));
```

### Multiple Return Values

```typescript
interface QueryResult {
  data: any;
  metadata: {
    count: number;
    page: number;
  };
}

const queryDatabase = captureResponse(
  async (query: string, page: number): Promise<QueryResult> => {
    // Database query implementation
    return {
      data: [],
      metadata: { count: 0, page }
    };
  }
);
```

## Troubleshooting

### Common Issues

1. **Type Validation Errors**
   - Ensure your response objects match the expected schema
   - Check that all required fields are present
   - Verify that field types match the schema definition

2. **Network Issues**
   - Verify that EVAL_TRACK_API_URL is correctly set
   - Check network connectivity to the eval-track server
   - Ensure proper CORS configuration if used in browser

3. **Memory Usage**
   - Large response objects may impact performance
   - Consider implementing response size limits
   - Monitor memory usage in production

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
DEBUG=eval-track:*
```

## Further Reading

For more detailed information about the tracer implementation and API reference, see the [official documentation](/docs/tracer.md).

## Contributing

Please refer to the project's contributing guidelines for information about making contributions to this package.
