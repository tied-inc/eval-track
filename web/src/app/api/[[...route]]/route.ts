import { logger } from "hono/logger";
import { requestId } from "hono/request-id";
import { secureHeaders } from "hono/secure-headers";
import { handle } from "hono/vercel";
import traces from "./traces";
import { getHonoApp } from "@/utils/hono";
import trackingIdMiddleware from "./middlewares/tracking-id-middleware";

export const runtime = "nodejs";

const app = getHonoApp().basePath("/api");

// Middlewares
app.use(logger());
app.use("*", requestId());
app.use("*", secureHeaders());
app.use("*", trackingIdMiddleware);

// Routes
app.get("/hello", (c) => {
	return c.json({
		message: "Hello Next.js!",
	});
});
const routes = app.route("/traces", traces);

export const GET = handle(app);
export const POST = handle(app);
export const PUT = handle(app);
export type AppType = typeof routes;
