import { inngest } from "@/utils/inngest/client";

export const healthFunction = {
	id: "health",
	event: "app/health",
};

export const health = inngest.createFunction(
	{ id: healthFunction.id },
	{ event: healthFunction.event },
	async ({ event, step }) => {
		await step.sleep("wait-a-moment", "1s");
		return { message: "ok" };
	},
);

export const sendHealthEvent = async () => {
	await inngest.send({
		name: healthFunction.event,
	});
};
