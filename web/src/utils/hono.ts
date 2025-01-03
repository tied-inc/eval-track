import { Hono } from "hono";
import type { RequestIdVariables } from "hono/request-id";
import { StorageType } from "@/utils/storage-client";

type HonoVariables = RequestIdVariables & {
	trackingId: string;
	artifactStoreType: StorageType;
};

export const getHonoApp = () => {
	return new Hono<{
		Variables: HonoVariables;
	}>();
};
