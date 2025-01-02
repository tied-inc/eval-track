import { zValidator } from "@hono/zod-validator";
import { Hono } from "hono";
import { z } from "zod";

import { inngestFunctions } from "@/app/api/inngest/functions";
import { inngest } from "@/utils/inngest/client";
import { PrismaClient } from "@prisma/client";

const app = new Hono();

app.get("/", async (c) => {
	const prisma = new PrismaClient();
	const ret = await prisma.trace.findMany();

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
	zValidator("json", postTraceSchema, async (result, c) => {
		console.log(result);
		console.log(await c.req.json());
		if (!result.success) {
			return c.text("Invalid!", 400);
		}
	}),
	async (c) => {
		await inngest.send({
			name: inngestFunctions.addTrace.event,
			data: {
				data: c.req.valid("json").data,
			},
		});

		return c.json({ status: 204 });
	},
);

export default app;
