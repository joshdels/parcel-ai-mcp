import * as maplibregl from "https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs";

export function createMap() {
  return new maplibregl.Map({
    container: "map",
    center: [-97.7, 30.6],
    zoom: 10,

    style: {
      version: 8,

      sources: {
        osm: {
          type: "raster",
          tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
          tileSize: 256,
        },
      },

      layers: [
        {
          id: "osm",
          type: "raster",
          source: "osm",
        },
      ],
    },
  });
}
