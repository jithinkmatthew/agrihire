function locationCascade(regionSelectId, districtSelectId, suburbSelectId, streetNameFieldId, cityFieldId, zipFieldId, existingRegionId, existingDistrictId, existingSuburbId) {
    const regionSelect = document.getElementById(regionSelectId);
    const districtSelect = document.getElementById(districtSelectId);
    const suburbSelect = document.getElementById(suburbSelectId);
    const streetNameField = document.getElementById(streetNameFieldId);
    const cityField = document.getElementById(cityFieldId);
    const zipField = document.getElementById(zipFieldId);

    let initialLoad = true;

    // Populate the initial region dropdown
    fetch('/regions')
        .then(response => response.json())
        .then(data => {
            regionSelect.innerHTML = '<option value="">Select a Region</option>';
            data.forEach(regions => {
                const option = document.createElement('option');
                option.value = regions.region_id;
                option.textContent = regions.name;
                regionSelect.appendChild(option);
            });

            if (existingRegionId) {
                regionSelect.value = existingRegionId;
            }

            else {
                districtSelect.innerHTML = '<option value="">Select a District</option>';
                suburbSelect.innerHTML = '<option value="">Select a Suburb</option>';
            }

            regionSelect.dispatchEvent(new Event('change')); // load suburbs

        });

    // Listen for changes on the region dropdown
    regionSelect.addEventListener('change', () => {

        console.log("region clicked")
        const regionId = regionSelect.value;
        districtSelect.innerHTML = '<option value="">Select a District</option>';
        suburbSelect.innerHTML = '<option value="">Select a Suburb</option>';
        console.log("region", streetNameField)

        if (!initialLoad) {
            streetNameField.value = '';
            cityField.value = '';
            zipField.value = '';
        }

        if (regionId) {
            // Fetch districts based on the selected region
            fetch(`/districts/${regionId}`)
                .then(response => response.json())
                .then(data => {
                    districtSelect.innerHTML = '<option value="">Select a District</option>';
                    data.forEach(district => {
                        const option = document.createElement('option');
                        option.value = district.district_id;
                        option.textContent = district.name;
                        districtSelect.appendChild(option);
                    });

                    if (initialLoad && existingDistrictId && data.some(sub => sub.district_id == existingDistrictId)) {
                        districtSelect.value = existingDistrictId;
                    } else {
                        // Reset selection to placeholder on change by user
                        districtSelect.value = "";
                        
                    }

                    districtSelect.dispatchEvent(new Event('change')); // load suburbs
                });
        }

        // initialLoad = false;
    });

    // Listen for changes on the suburb dropdown
    districtSelect.addEventListener('change', () => {
        console.log("district selected")
        const districtId = districtSelect.value;
        suburbSelect.innerHTML = '<option value="">Select a Suburb</option>';

        if (districtId) {
            // Fetch districts based on the selected region
            fetch(`/suburbs/${districtId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(suburb => {
                        const option = document.createElement('option');
                        option.value = suburb.suburb_id;
                        option.textContent = suburb.name;
                        suburbSelect.appendChild(option);
                    });

                    if (existingSuburbId && data.some(sub => sub.suburb_id == existingSuburbId)) {
                        suburbSelect.value = existingSuburbId;
                    } else {
                        // Reset selection to placeholder on change by user
                        suburbSelect.value = "";
                    }


                });

        }
        initialLoad = false;
    });
}


function searchLocationCascade(regionSelectId, districtSelectId, suburbSelectId) {
    const regionSelect = document.getElementById(regionSelectId);
    const districtSelect = document.getElementById(districtSelectId);
    const suburbSelect = document.getElementById(suburbSelectId);

    const regionId = regionSelect.value;
    const districtId = districtSelect.value;
    const suburbId = suburbSelect.value;

    // Fetching value when coming back to the search result
    if (regionId !== '0') {
        
        fetch(`/districts/${regionId}`)
            .then(response => response.json())
            .then(data => {
                // let districtOptions;
                let districtOptions = '<option value="0" selected>All Districts</option>';
                data.forEach(district => {
                    districtOptions += `<option value="${district.district_id}">${district.name}</option>`;
                });

                districtSelect.innerHTML = districtOptions;    
                districtSelect.value = districtId;                
            });
    }

    // Listen for changes on the region dropdown
    regionSelect.addEventListener('change', () => {

        const regionId = regionSelect.value;
        if (regionId != null) {
            // Fetch districts based on the selected region
            fetch(`/districts/${regionId}`)
                .then(response => response.json())
                .then(data => {
                    let districtOptions = '<option value="0" selected>All Districts</option>';
                    data.forEach(district => {
                        districtOptions += `<option value="${district.district_id}">${district.name}</option>`;
                    });

                    districtSelect.innerHTML = districtOptions;                    
                });
        } 
    });
    
    // Fetch districts when coming back to the search result
    if (districtId !== '0') {
            // Fetch districts based on the selected region
            fetch(`/suburbs/${districtId}`)
                .then(response => response.json())
                .then(data => {
                    let suburbOptions = '<option value="0" selected>All Suburbs</option>';
                    data.forEach(suburb => {
                        suburbOptions += `<option value="${suburb.suburb_id}">${suburb.name}</option>`;
                    });
                    suburbSelect.innerHTML = suburbOptions;
                    suburbSelect.value = suburbId;                

                });
        }

    // Listen for changes on the suburb dropdown
    districtSelect.addEventListener('change', () => {
        const districtId = districtSelect.value;
        if (districtId !== null) {
            // Fetch districts based on the selected region
            fetch(`/suburbs/${districtId}`)
                .then(response => response.json())
                .then(data => {
                    let suburbOptions = '<option value="0" selected>All Suburbs</option>';
                    data.forEach(suburb => {
                        suburbOptions += `<option value="${suburb.suburb_id}">${suburb.name}</option>`;
                    });
                    suburbSelect.innerHTML = suburbOptions;

                });
        }
    });
}

// Location  - Cascade functionality
document.addEventListener('DOMContentLoaded', () => {

    // Add Equipment
    document.querySelectorAll('.add_equipment').forEach(form => {
        locationCascade(
            "add_equipment_region", 
            "add_equipment_district",
            "add_equipment_suburb",
            "add_equipment_street_name",
            "add_equipment_city",
            "add_equipment_zip",
            null,null,null
        );

    });

    // Add land
    document.querySelectorAll('.add_land').forEach(form => {
        locationCascade(
            "add_land_region", 
            "add_land_district",
            "add_land_suburb",
            "add_land_street_name",
            "add_land_city",
            "add_land_zip",
            null,null,null
        );

    });
    
    // Edit Equipment
    document.querySelectorAll('.edit_equipment_form').forEach(form => {
        const equipmentId = form.dataset.equipmentId;
        console.log("equipmentId-Edit", equipmentId)
        const existingRegionId = form.dataset.existingRegionId;
        const existingDistrictId = form.dataset.existingDistrictId;
        const existingSuburbId = form.dataset.existingSuburbId;

        console.log(existingRegionId, existingDistrictId, existingSuburbId)

        const editRegionSelectId = 'edit_equip_region_' + equipmentId;
        const edit_districtSelectId = `edit_equip_district_${equipmentId}`;
        const edit_suburbSelectId = `edit_equip_suburb_${equipmentId}`;
        const edit_streetNameFieldId = `edit_equip_street_${equipmentId}`;
        const edit_cityFieldId = `edit_equip_city_${equipmentId}`;
        const edit_zipFieldId = `edit_equip_zip_${equipmentId}`;

        console.log("before", editRegionSelectId)

        locationCascade(
            editRegionSelectId,
            edit_districtSelectId,
            edit_suburbSelectId,
            edit_streetNameFieldId,
            edit_cityFieldId,
            edit_zipFieldId,
            existingRegionId,
            existingDistrictId,
            existingSuburbId
        );

    });

    // Edit Land
    document.querySelectorAll('.edit_land_form').forEach(form => {
        const landId = form.dataset.landId;
        const existingRegionId = form.dataset.existingRegionId;
        const existingDistrictId = form.dataset.existingDistrictId;
        const existingSuburbId = form.dataset.existingSuburbId;
        console.log("HHHH-----", landId)
        // console.log(existingRegionId, existingDistrictId, existingSuburbId)

        const editRegionSelectId = 'edit_land_region_' + landId;
        const edit_districtSelectId = `edit_land_district_${landId}`;
        const edit_suburbSelectId = `edit_land_suburb_${landId}`;
        const edit_streetNameFieldId = `edit_land_street_${landId}`;
        const edit_cityFieldId = `edit_land_city_${landId}`;
        const edit_zipFieldId = `edit_land_zip_${landId}`;

        // console.log("before", editRegionSelectId)

        locationCascade(
            editRegionSelectId,
            edit_districtSelectId,
            edit_suburbSelectId,
            edit_streetNameFieldId,
            edit_cityFieldId,
            edit_zipFieldId,
            existingRegionId,
            existingDistrictId,
            existingSuburbId
        );

    });

    // Equipment Search 
    document.querySelectorAll('.equip_search_form').forEach(form => {
        searchLocationCascade(
            "equip_search_region",
            "equip_search_district",
            "equip_search_suburb"
        );
    });

    // Land Search
    document.querySelectorAll('.land_search_form').forEach(form => {
        searchLocationCascade(
            "land_search_region",
            "land_search_district",
            "land_search_suburb"
        );
    });


});
