let map;

function locateMap(
  mapId,
  eqp_regionId,
  eqp_districtId,
  eqp_suburbId,
  eqp_street_nameId,
  eqp_location_cityId,
  eqp_location_zipId,
  eqp_location_coordinatesId,
  eqp_get_coordinates_btnId) {

  const eqp_region = document.getElementById(eqp_regionId);
  const eqp_district = document.getElementById(eqp_districtId);
  const eqp_suburb = document.getElementById(eqp_suburbId);
  const eqp_street_name = document.getElementById(eqp_street_nameId);
  const eqp_location_city = document.getElementById(eqp_location_cityId);
  const eqp_location_zip = document.getElementById(eqp_location_zipId);
  const eqp_location_coordinates = document.getElementById(eqp_location_coordinatesId);
  const eqp_get_coordinates_btn = document.getElementById(eqp_get_coordinates_btnId);

  if (map) {
    map.off();          
    map.remove();       // Remove existing map instance
    map = null;         // Clear the variable
  }
  
  if (!map) {
     map = L.map(mapId, {
      zoomControl: false,
      scrollWheelZoom: false,
      doubleClickZoom: true,
      dragging: true,
    });

    map.setView([-40.9, 174.8], 4);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',}).addTo(map);

    let marker;

    if (eqp_get_coordinates_btn) {
      
      eqp_get_coordinates_btn.addEventListener("click", (event) => {
        event.preventDefault();
        console.log("button clicked");
        const selectedRegion = eqp_region.options[eqp_region.selectedIndex].textContent;
        const selectedDistrict = eqp_district.options[eqp_district.selectedIndex].textContent;
        const selectedSuburbs = eqp_suburb.options[eqp_suburb.selectedIndex].textContent;
        const address = `${eqp_street_name.value}, ${selectedSuburbs}, ${eqp_location_city.value}, ${selectedRegion}, ${selectedDistrict}, ${eqp_location_zip.value} `;
        console.log(address);

        const geocodingUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
          address
        )}`;
        fetch(geocodingUrl)
          .then((response) => response.json())
          .then((data) => {
            console.log("data", data);
            if (data.length > 0) {
              const lat = parseFloat(data[0].lat);
              const lon = parseFloat(data[0].lon);
              eqp_location_coordinates.value = `${lat}, ${lon}`;
              console.log("J--", eqp_location_coordinates.value);
              if (marker) {
                map.removeLayer(marker);
              }
              map.setView([lat, lon], 10);
              marker = L.marker([lat, lon])
                .addTo(map)
                .bindPopup(data[0].display_name)
                .openPopup();
            } else {
              alert("Location not found. Please try a different address.");
            }
          })
          .catch((error) => {
            console.error("Geocoding error:", error);
            alert("An error occurred during geocoding.");
          });
      });
    }

    const addEquipTab = document.getElementById("pills-add-tab");
    if (addEquipTab) {
      addEquipTab.addEventListener("click", () => {
        // Use a slight delay to give the tab time to become visible
        setTimeout(() => {
          map.invalidateSize();
        }, 300);
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", (event) => {
  locateMap(
    "map",
    "add_equipment_region",
    "add_equipment_district",
    "add_equipment_suburb",
    "add_equipment_street_name",
    "add_equipment_city",
    "add_equipment_zip",
    "add_equip_geo_coordinate",
    "add_equip_get_coordinates_btn"
  );

    locateMap(
    "map",
    "add_land_region",
    "add_land_district",
    "add_land_suburb",
    "add_land_street_name",
    "add_land_city",
    "add_land_zip",
    "add_land_geo_coordinate",
    "add_land_get_coordinates_btn"
  );

});

// Map view in view equipment page
document.addEventListener("DOMContentLoaded", function () {
  // const gps_coordinate = document.getElementById('map_view');
  // document.querySelectorAll('[id^="previewModal_"]').forEach(modal => {
  // modal.addEventListener("shown.bs.modal", function () {
  // const eqpId = modal.id.split("_")[1];
  // const mapId = "map_" + eqpId;
  const mapContainer = document.getElementById("map_view");
  console.log("mapContainer", mapContainer);
  if (!mapContainer) {
    console.error("Map container not found:");
    return;
  }
  // Avoid duplicate maps
  if (mapContainer.dataset.mapInit) return;
  mapContainer.dataset.mapInit = true;
  const lat = parseFloat(mapContainer.dataset.lat);
  const lon = parseFloat(mapContainer.dataset.lon);
  const map = L.map(mapContainer, {
    zoomControl: false,
    center: [lat, lon],
    zoom: 15,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    dragging: true
  });
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
  }).addTo(map);

  L.circle([lat, lon], {
    radius: 200,
    color: "#4078f2",
    fillColor: "#4078f2",
    fillOpacity: 0.2
  }).addTo(map);
});

// Map view in Edit Equipment
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('[id^="previewModal_"]').forEach((modal) => {
    modal.addEventListener("shown.bs.modal", function () {
      const eqpId = modal.id.split("_")[1];
      const mapId = "map_" + eqpId;
      const mapContainer = document.getElementById(mapId);
      if (!mapContainer) {
        console.error("Map container not found:", mapId);
        return;
      }
      // Avoid duplicate maps
      if (mapContainer.dataset.mapInit) return;
      mapContainer.dataset.mapInit = true;
      const lat = parseFloat(modal.dataset.lat);
      const lon = parseFloat(modal.dataset.lon);
      const map = L.map(mapId, {
        zoomControl: false,
        center: [lat, lon],
        zoom: 15,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        dragging: true,
      });
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
      }).addTo(map);
      L.circle([lat, lon], {
        radius: 200, // in meters
        color: "#4078f2",
        fillColor: "#4078f2",
        fillOpacity: 0.2,
      }).addTo(map);
    });
  });
});

// Edit Equipment
document.addEventListener("DOMContentLoaded", () => {
  const modals = document.querySelectorAll('[id^="editModal_"]');

  modals.forEach((modal) => {
    modal.addEventListener("shown.bs.modal", () => {
      const eqpId = modal.id.split("_")[1];
      const mapId = "map_" + eqpId;
      const mapContainer = document.getElementById(mapId);

      if (!mapContainer) {
        console.error("Map container not found:", mapId);
        return;
      }

      // Initialize map once
      if (!mapContainer.dataset.mapInit) {
        mapContainer.dataset.mapInit = true;

        const lat = parseFloat(modal.dataset.lat);
        const lon = parseFloat(modal.dataset.lon);

        const map = L.map(mapId, {
          zoomControl: false,
          center: [lat, lon],
          zoom: 15,
          scrollWheelZoom: false,
          doubleClickZoom: false,
          dragging: true,
        });

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
        }).addTo(map);

        L.circle([lat, lon], {
          radius: 200,
          color: "#4078f2",
          fillColor: "#4078f2",
          fillOpacity: 0.2
        }).addTo(map);

        setTimeout(() => map.invalidateSize(), 200);

        // Attach GPS button handler only once
        const getGpsBtn = modal.querySelector(`#edit_equip_getcoordinate_btn_${eqpId}`);
        console.log(getGpsBtn);
        if (getGpsBtn) {
          let marker; // scoped to this modal

          getGpsBtn.addEventListener("click", async (e) => {
              e.preventDefault();

              const region = modal.querySelector(`#edit_equip_region_${eqpId}`);
              const district = modal.querySelector(`#edit_equip_district_${eqpId}`);
              const suburb = modal.querySelector(`#edit_equip_suburb_${eqpId}`);
              const street = modal.querySelector(`#edit_equip_street_${eqpId}`);
              const city = modal.querySelector(`#edit_equip_city_${eqpId}`);
              const zip = modal.querySelector(`#edit_equip_zip_${eqpId}`);
              const coordsField = modal.querySelector(`#edit_equip_gpscoordinate_${eqpId}`);

              const address = `${street?.value || ""}, 
              ${suburb?.options[suburb.selectedIndex]?.textContent || ""}, 
              ${city?.value || ""}, 
              ${region?.options[region.selectedIndex]?.textContent || ""}, 
              ${district?.options[district.selectedIndex]?.textContent || ""}, 
              ${zip?.value || ""}`.replace(/\s+/g, " ").trim();

              console.log("Edit Geocoding address:", address);

              try {
                const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
                const data = await response.json();

                if (data.length > 0) {
                  const lat = parseFloat(data[0].lat);
                  const lon = parseFloat(data[0].lon);

                  coordsField.value = `${lat}, ${lon}`;
                  console.log("Coordinates set:", coordsField.value);

                  if (marker) {
                    map.removeLayer(marker);
                  }
                  map.setView([lat, lon], 16);
                  marker = L.marker([lat, lon])
                    .addTo(map)
                    .bindPopup(data[0].display_name)
                    .openPopup();
                } else {
                  alert("Location not found. Please try a different address.");
                }
              } catch (error) {
                console.error("Geocoding error:", error);
                alert("An error occurred during geocoding.");
              }
            },
            { once: false }
          ); // keep it reusable while modal is open
        }
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const modals = document.querySelectorAll('[id^="landEditModal_"]');

  modals.forEach((modal) => {
    const landId = modal.id.split("_")[1];
    const mapId = "map_" + landId;
    const mapContainer = document.getElementById(mapId);

    modal.addEventListener("shown.bs.modal", () => {
      if (!mapContainer) {
        console.error("Map container not found:", mapId);
        return;
      }

      // Prevent initializing the map multiple times
      if (mapContainer.dataset.mapInit) return;

      mapContainer.dataset.mapInit = true;

      const lat = parseFloat(modal.dataset.lat);
      const lon = parseFloat(modal.dataset.lon);

      const map = L.map(mapId, {
        zoomControl: false,
        center: [lat, lon],
        zoom: 15,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        dragging: true,
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
      }).addTo(map);

      L.circle([lat, lon], {
        radius: 200,
        color: "#4078f2",
        fillColor: "#4078f2",
        fillOpacity: 0.2
      }).addTo(map);

      setTimeout(() => map.invalidateSize(), 200);

      // Attach GPS button handler
      const getGpsBtn = modal.querySelector(`#edit_land_geo_coordinate_btn_${landId}`);
      console.log(getGpsBtn);
      if (getGpsBtn) {
        let marker; // scoped to this modal

        getGpsBtn.addEventListener("click", async (e) => {
          e.preventDefault();

          const region = modal.querySelector(`#edit_land_region_${landId}`);
          const district = modal.querySelector(`#edit_land_district_${landId}`);
          const suburb = modal.querySelector(`#edit_land_suburb_${landId}`);
          const street = modal.querySelector(`#edit_land_street_${landId}`);
          const city = modal.querySelector(`#edit_land_city_${landId}`);
          const zip = modal.querySelector(`#edit_land_zip_${landId}`);
          const coordsField = modal.querySelector(`#edit_land_geo_coordinate_${landId}`);

          const address = `${street?.value || ""}, 
            ${suburb?.options[suburb.selectedIndex]?.textContent || ""}, 
            ${city?.value || ""}, 
            ${region?.options[region.selectedIndex]?.textContent || ""}, 
            ${district?.options[district.selectedIndex]?.textContent || ""}, 
            ${zip?.value || ""}`.replace(/\s+/g, " ").trim();

          console.log("Edit Geocoding address:", address);

          try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
            const data = await response.json();

            if (data.length > 0) {
              const lat = parseFloat(data[0].lat);
              const lon = parseFloat(data[0].lon);

              coordsField.value = `${lat}, ${lon}`;
              console.log("Coordinates set:", coordsField.value);

              if (marker) {
                map.removeLayer(marker);
              }
              map.setView([lat, lon], 16);
              marker = L.marker([lat, lon])
                .addTo(map)
                .bindPopup(data[0].display_name)
                .openPopup();
            } else {
              alert("Location not found. Please try a different address.");
            }
          } catch (error) {
            console.error("Geocoding error:", error);
            alert("An error occurred during geocoding.");
          }
        }, { once: false });
      }
    });

    // Reset map initialization flag and clear map on modal close
    modal.addEventListener("hidden.bs.modal", () => {
      if (mapContainer) {
        delete mapContainer.dataset.mapInit;
        mapContainer.innerHTML = ""; // clear previous map instance
      }
    });
  });
});
