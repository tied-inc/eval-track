import {createMiddleware} from 'hono/factory';
import { v4 as uuidv4 } from "uuid";

const trackingIdMiddleware = createMiddleware(async (c, next) => {
	let trackingId = c.req.header("x-eval-track-tracking-id");
	if (!trackingId) {
		trackingId = uuidv4();
	}
	c.set("trackingId", trackingId);

	await next();

	c.res.headers.set("x-eval-track-tracking-id", trackingId);
	c.res.headers.set("x-eval-track-trace-id", c.get("requestId"));
})

export default trackingIdMiddleware;