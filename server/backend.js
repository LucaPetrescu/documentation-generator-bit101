import { GenezioDeploy } from "@genezio/types";
import fetch from "node-fetch";

@GenezioDeploy()
export class BackendService {
  async hello(name) {
    const ipLocation = await fetch("http://ip-api.com/json/")
      .then((res) => res.json())
      .catch(() => ({ status: "fail" }));

    if (ipLocation.status === "fail") {
      return `Hello ${name}! Failed to get the server location :(`;
    }

    const formattedTime = new Date().toLocaleString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });

    return `Hello ${name}! This response was served from ${ipLocation.city}, ${ipLocation.country} (${ipLocation.lat}, ${ipLocation.lon}) at ${formattedTime}`;
  }
}
