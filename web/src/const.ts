export const settings = {
	baseUrl: process.env.BASE_URL || "http://localhost:3000",
};

// Inngest Info
export const inngestSettings = {
	clientId: process.env.INNGEST_CLIENT_ID || "eval-track",
	eventKey: process.env.INNGEST_EVENT_KEY || "",
	signingKey: process.env.INNGEST_SIGNING_KEY || "",
};
