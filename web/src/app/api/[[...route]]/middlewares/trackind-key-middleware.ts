import { createMiddleware } from 'hono/factory';
import { HTTPException } from 'hono/http-exception';
import prisma from '@/utils/prisma';


const trackingKeyMiddleware = createMiddleware(async (c, next) => {
  const key = c.req.header("x-eval-track-tracking-key");
  if (!key) {
    throw new HTTPException(401, {message: 'Missing tracking key'});
  }

  // redis is better?
  const ret = await prisma.applicationTrackingKey.findUnique({
      where: {
        key,
        isActive: true,
      },
    include: {
        Application: {
          include: {
            ArtifactStore: true
          }
        },
    }
    });

  if (!ret) {
    throw new HTTPException(401, {message: 'Invalid tracking key'});
  }

  const artifactStore = ret.Application.ArtifactStore.type
  c.set('artifactStoreType', artifactStore)

  await next();

})

export default trackingKeyMiddleware;