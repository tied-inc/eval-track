import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

import { sendAddTraceEvent } from "@/worker/add-trace";
import { PrismaClient } from "@prisma/client";
import { getHonoApp } from "@/utils/hono";
import { getStorageClient } from "@/utils/storage-client";

const app = getHonoApp();

app.get("/", async (c) => {
	const prisma = new PrismaClient();
	const ret = await prisma.applicationTrace.findMany();

	return c.json({
		status: 200,
		data: ret,
	});
});

const postTraceSchema = z.object({
	data: z.string(),
});
app.post(
	"/",
	zValidator("json", postTraceSchema),
	async (c) => {
		const storage = getStorageClient();

		// todo: store data to storage before sending event
		await sendAddTraceEvent({
			trackingId: c.get("trackingId"),
			traceId: c.get("requestId"),
			data: c.req.valid("json").data,
		});

		return c.json({ status: 204 });
	},
);

export default app;
