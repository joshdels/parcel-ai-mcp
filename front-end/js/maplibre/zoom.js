import * as maplibregl from "https://unpkg.com/maplibre-gl@^6.0.0/dist/maplibre-gl.mjs";

export async function zoomToParcel(map, parcelId) {
  const response = await fetch(`http://127.0.0.1:8000/parcel/${parcelId}`);

  if (!response.ok) {
    console.error(`Parcel ${parcelId} not found.`);
    return;
  }

  const parcel = await response.json();

  // Highlight parcel
  const source = map.getSource("selected-parcel");

  source.setData({
    type: "Feature",
    properties: {
      prop_id: parcel.prop_id,
    },
    geometry: parcel.geometry,
  });

  // Get coordinates
  const coordinates = [];

  function collectCoordinates(coords) {
    if (typeof coords[0] === "number") {
      coordinates.push(coords);
      return;
    }

    for (const coord of coords) {
      collectCoordinates(coord);
    }
  }

  collectCoordinates(parcel.geometry.coordinates);

  if (!coordinates.length) {
    console.error(`No coordinates found for ${parcelId}.`);
    return;
  }

  const bounds = coordinates.reduce(
    (bounds, coordinate) => bounds.extend(coordinate),
    new maplibregl.LngLatBounds(coordinates[0], coordinates[0]),
  );

  map.fitBounds(bounds, {
    padding: 80,
    duration: 1000,
    maxZoom: 18,
  });
}
