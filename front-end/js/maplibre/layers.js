import * as maplibregl from "https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs";

export function loadLayer(map) {
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

  map.on("mouseenter", "parcels-fill", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseleave", "parcels-fill", () => {
    map.getCanvas().style.cursor = "";
  });

  map.on("click", "parcels-fill", async (event) => {
    const feature = event.features?.[0];

    if (!feature) {
      return;
    }

    const propId = feature.properties?.prop_id;
    const propOwner = feature.properties?.owner_name;
    const propVal = feature.properties?.mkt_value;
    const propSitus = feature.properties?.situs_addr;

    console.log(propId, propOwner);

    if (!propId) {
      console.error("Clicked parcel has no prop_id.");
      return;
    }

    // Get the authoritative parcel geometry from FastAPI
    const response = await fetch(`http://127.0.0.1:8000/parcel/${propId}`);

    if (!response.ok) {
      console.error(`Parcel ${propId} not found.`);
      return;
    }

    const parcel = await response.json();

    // Use the SAME selection mechanism as zoomToParcel()
    const selectedFeature = {
      type: "Feature",
      properties: {
        prop_id: parcel.prop_id,
        owner_name: parcel.owner_name,
        mkt_value: parcel.mkt_value,
        situs_addr: parcel.situs_addr,
      },
      geometry: parcel.geometry,
    };

    selectParcel(map, selectedFeature);

    new maplibregl.Popup()
      .setLngLat(event.lngLat)
      .setHTML(
        `
      <strong>Property ID</strong><br>
      ${propId ?? "Unknown"}<br>

      ${propOwner ?? "Unknown"}<br>

      $ ${propVal ?? "Unknown"}<br>

      ${propSitus ?? "Unknown"}<br>
      `,
      )
      .addTo(map);
  });
}

/**
 * Set the single orange selected parcel.
 *
 * Everything that wants to highlight a parcel should
 * use this function.
 */
export function selectParcel(map, feature) {
  const source = map.getSource("selected-parcel");

  if (!source) {
    console.error("selected-parcel source not found.");
    return;
  }

  source.setData({
    type: "Feature",
    properties: feature.properties ?? {},
    geometry: feature.geometry,
  });
}

/**
 * Remove the orange selected parcel.
 */
export function clearSelectedParcel(map) {
  const source = map.getSource("selected-parcel");

  if (!source) {
    return;
  }

  source.setData({
    type: "FeatureCollection",
    features: [],
  });
}

export function loadSelectedParcelLayer(map) {
  map.addSource("selected-parcel", {
    type: "geojson",
    data: {
      type: "FeatureCollection",
      features: [],
    },
  });

  map.addLayer({
    id: "selected-parcel-fill",
    type: "fill",
    source: "selected-parcel",
    minzoom: 12,
    paint: {
      "fill-color": "#ff8c00",
      "fill-opacity": 0.45,
    },
  });

  map.addLayer({
    id: "selected-parcel-outline",
    type: "line",
    source: "selected-parcel",
    minzoom: 12,
    paint: {
      "line-color": "#ff8c00",
      "line-width": 3,
    },
  });
}
