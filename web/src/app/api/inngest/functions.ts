import { inngest } from "@/utils/inngest/client";
import prisma from "@/utils/prisma";

export const inngestFunctions = {
	health: {
		id: "health",
		event: "app/health",
	},
	addTrace: {
		id: "addTrace",
		event: "app/add.trace",
	},
};

const health = inngest.createFunction(
	{ id: inngestFunctions.health.id },
	{ event: inngestFunctions.health.event },
	async ({ event, step }) => {
		await step.sleep("wait-a-moment", "1s");
		return { message: "ok" };
	},
);

const addTrace = inngest.createFunction(
	{ id: inngestFunctions.addTrace.id },
	{ event: inngestFunctions.addTrace.event },
	async ({ event, step }) => {
		prisma.trace.create({
			data: {},
		});

		return {};
	},
);

export const functions = [health, addTrace];
