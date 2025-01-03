import { inngest } from "@/utils/inngest/client";
import { z } from "zod";

export const analyzeArtifactFunction = {
	id: "analyzeArtifact",
	event: "app/analyze.artifact",
};

const analyzeArtifactSchema = z.object({});
export type AnalyzeArtifactSchema = z.infer<typeof analyzeArtifactSchema>;

export const analyzeArtifact = inngest.createFunction(
	{ id: analyzeArtifactFunction.id },
	{ event: analyzeArtifactFunction.event },
	async ({ event, step }) => {
		return {};
	},
);

export const sendAnalyzeArtifactEvent = async (data: AnalyzeArtifactSchema) => {
	await inngest.send({ name: analyzeArtifactFunction.event, data });
};
