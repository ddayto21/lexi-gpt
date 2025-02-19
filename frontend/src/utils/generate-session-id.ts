import { v4 as uuidv4 } from "uuid";

export const generateSessionId = (): string => {
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, "");

  const uuid = uuidv4().split("-")[0];

  return `session-${timestamp}-${uuid}`;
};
