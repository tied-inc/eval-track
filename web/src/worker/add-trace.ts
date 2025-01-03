import { inngest } from "@/utils/inngest/client";

import { z } from "zod";

const addTraceSchema = z.object({
	trackingId: z.string().uuid(),
	traceId: z.string().uuid(),
	data: z.string(),
});
export type AddTraceSchema = z.infer<typeof addTraceSchema>;
export const addTraceFunction = {
	id: "addTrace",
	event: "app/add.trace",
	schema: addTraceSchema,
};
export const addTrace = inngest.createFunction(
	{ id: addTraceFunction.id },
	{ event: addTraceFunction.event },
	async ({ event, step }) => {
		// todo: add create trace logic
		return {};
	},
);
export const sendAddTraceEvent = async (data: AddTraceSchema) => {
	await inngest.send({
		name: addTraceFunction.event,
		data,
	});
};
