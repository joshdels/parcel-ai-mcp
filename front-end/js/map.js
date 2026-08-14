import * as maplibregl from "https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs";

export const map = new maplibregl.Map({
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

map.on("load", () => {
  map.addSource("parcels", {
    type: "vector",
    tiles: ["http://127.0.0.1:8000/tiles/{z}/{x}/{y}.pbf"],
    minzoom: 10,
    maxzoom: 20,
  });

  map.addLayer({
    id: "parcels-fill",
    type: "fill",
    source: "parcels",
    "source-layer": "williamson_parcels",
    minzoom: 12,
    paint: {
      "fill-color": "#0080ff",
      "fill-opacity": 0.25,
    },
  });

  map.addLayer({
    id: "parcels-outline",
    type: "line",
    source: "parcels",
    "source-layer": "williamson_parcels",
    minzoom: 10,
    paint: {
      "line-color": "#0080ff",
      "line-width": 1,
      "line-opacity": 0.6,
    },
  });

  // Change cursor when hovering over a parcel.
  map.on("mouseenter", "parcels-fill", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseleave", "parcels-fill", () => {
    map.getCanvas().style.cursor = "";
  });

  // Click parcel.
  map.on("click", "parcels-fill", (event) => {
    const feature = event.features?.[0];

    if (!feature) {
      return;
    }

    const propId = feature.properties?.prop_id;

    new maplibregl.Popup()
      .setLngLat(event.lngLat)
      .setHTML(
        `
        <strong>Property ID</strong><br>
        ${propId ?? "Unknown"}
      `,
      )
      .addTo(map);
  });
});
