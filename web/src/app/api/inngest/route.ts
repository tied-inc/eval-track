import { serve } from "inngest/next";
import { inngest } from "@/utils/inngest/client";
import { functions } from "@/app/api/inngest/functions";

// Create an API that serves zero functions
export const { GET, POST, PUT } = serve({
	client: inngest,
	functions,
});
