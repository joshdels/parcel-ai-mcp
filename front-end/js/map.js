import * as maplibregl from "https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs";

export const map = new maplibregl.Map({
  container: "map",
  style:
    "https://raw.githubusercontent.com/go2garret/maps/main/src/assets/json/openStreetMap.json",
  center: [0, 0],
  zoom: 2,
});
