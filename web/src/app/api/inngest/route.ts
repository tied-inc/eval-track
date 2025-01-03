import { serve } from "inngest/next";
import { inngest } from "@/utils/inngest/client";
import workers from "@/worker";

// Create an API that serves zero functions
export const { GET, POST, PUT } = serve({
	client: inngest,
	functions: workers,
});
