import { settings } from "@/const";
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
	baseURL: settings.baseUrl,
});
