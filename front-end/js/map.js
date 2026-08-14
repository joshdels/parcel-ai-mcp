import { createMap } from "./maplibre/createMap.js";
import { loadLayer, loadSelectedParcelLayer } from "./maplibre/layers.js";
import { zoomToParcel } from "./maplibre/zoom.js";
import { connectWebSocket, sendCommand } from "./websocket.js";

const map = createMap();

let socket;

map.on("load", () => {
  console.log("Map loaded");

  loadLayer(map);
  loadSelectedParcelLayer(map);

  socket = connectWebSocket(async (message) => {
    if (message.action === "zoom_to_parcel") {
      await zoomToParcel(map, message.parcel_id);
    }
  });

  socket.addEventListener("open", () => {
    sendCommand(socket, {
      action: "zoom_to_parcel",
      parcel_id: "R039385",
    });
  });
});
