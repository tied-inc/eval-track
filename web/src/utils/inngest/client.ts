import { inngestSettings } from "@/const";
import { Inngest } from "inngest";

export const inngest = new Inngest({ id: inngestSettings.clientId });
