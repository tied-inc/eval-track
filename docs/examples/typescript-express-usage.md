# Advanced TypeScript Usage with Express.js

This example demonstrates how to use the TypeScript tracer with Express.js, showing function response capture across multiple endpoints and middleware.

## Installation

```bash
pnpm add express @tied-inc/eval-track @types/express
```

## Basic Express.js Integration

```typescript
import express from 'express';
import { captureResponse } from '@tied-inc/eval-track';
import { z } from 'zod';

const app = express();
app.use(express.json());

// Define response schemas
const ServiceResponse = z.object({
  message: z.string(),
  timestamp: z.number(),
});

type ServiceResponse = z.infer<typeof ServiceResponse>;

// Create traced middleware
const tracedMiddleware = (handler: express.RequestHandler): express.RequestHandler => {
  const wrapped = captureResponse(handler);
  return async (req, res, next) => {
    try {
      await wrapped(req, res, next);
    } catch (error) {
      next(error);
    }
  };
};

// Service endpoints
app.get('/service1', tracedMiddleware(async (req, res) => {
  const response: ServiceResponse = {
    message: 'Service 1 response',
    timestamp: Date.now(),
  };
  res.json(response);
}));

app.get('/service2', tracedMiddleware(async (req, res) => {
  const response: ServiceResponse = {
    message: 'Service 2 response',
    timestamp: Date.now(),
  };
  res.json(response);
}));

// Orchestration endpoint
const OrchestrationResponse = z.object({
  service1: ServiceResponse,
  service2: ServiceResponse,
  orchestratedAt: z.number(),
});

type OrchestrationResponse = z.infer<typeof OrchestrationResponse>;

app.get('/orchestrate', tracedMiddleware(async (req, res) => {
  // Make internal requests to services
  const [service1Data, service2Data] = await Promise.all([
    fetch('http://localhost:3000/service1').then(r => r.json()),
    fetch('http://localhost:3000/service2').then(r => r.json()),
  ]);

  const response: OrchestrationResponse = {
    service1: service1Data,
    service2: service2Data,
    orchestratedAt: Date.now(),
  };

  res.json(response);
}));

// Error handling middleware
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    error: err.message,
    timestamp: Date.now(),
  });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

## Advanced Error Handling

```typescript
// Custom error class
class ServiceError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'ServiceError';
  }
}

// Enhanced middleware with error handling
const tracedErrorHandler = (handler: express.RequestHandler): express.RequestHandler => {
  const wrapped = captureResponse(async (req, res, next) => {
    try {
      await handler(req, res, next);
    } catch (error) {
      if (error instanceof ServiceError) {
        res.status(error.statusCode).json({
          error: error.message,
          context: error.context,
          timestamp: Date.now(),
        });
      } else {
        next(error);
      }
    }
  });

  return (req, res, next) => {
    wrapped(req, res, next).catch(next);
  };
};

// Usage with custom error handling
app.get('/risky-service', tracedErrorHandler(async (req, res) => {
  const shouldFail = Math.random() > 0.5;
  
  if (shouldFail) {
    throw new ServiceError('Service temporarily unavailable', 503, {
      retryAfter: 30,
    });
  }

  res.json({
    message: 'Service successful',
    timestamp: Date.now(),
  });
}));
```

## Request Context Tracking

```typescript
// Define request context type
interface RequestContext {
  requestId: string;
  userId?: string;
  startTime: number;
}

// Create context middleware
const contextMiddleware: express.RequestHandler = (req, res, next) => {
  const context: RequestContext = {
    requestId: crypto.randomUUID(),
    userId: req.headers['x-user-id'] as string,
    startTime: Date.now(),
  };
  
  res.locals.context = context;
  next();
};


// Enhanced tracer middleware with context
const tracedContextHandler = (handler: express.RequestHandler): express.RequestHandler => {
  const wrapped = captureResponse(async (req, res, next) => {
    const context = res.locals.context as RequestContext;
    const result = await handler(req, res, next);
    
    // Add context to trace data
    return {
      ...result,
      _context: context,
      _duration: Date.now() - context.startTime,
    };
  });

  return (req, res, next) => {
    wrapped(req, res, next).catch(next);
  };
};

// Usage with context
app.use(contextMiddleware);

app.get('/contextual-service', tracedContextHandler(async (req, res) => {
  const context = res.locals.context as RequestContext;
  
  res.json({
    message: `Request ${context.requestId} processed`,
    userId: context.userId,
    timestamp: Date.now(),
  });
}));
```

This example demonstrates:
1. Basic Express.js integration with traced endpoints
2. Request orchestration across multiple services
3. Advanced error handling with custom error types
4. Request context tracking and duration measurement
5. Type safety with Zod schemas
6. Middleware composition for tracing and context

The tracer captures all responses and errors automatically, providing observability across the entire request lifecycle.
