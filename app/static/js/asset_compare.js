function compare_equipment() {
  const fields = ['name', 'category_name', 'description', 'make', 'model', 'year', 'price', 'price_modal'];
  compare_assets_core('.equip-compare-checkbox', 'equipCompareBtn', 'equipClearCompareBtn', 'equipment', 'equipCompareContent', 'equipCompareModal', fields);
}

function compare_land() {
  const fields = ['name', 'category_name', 'description', 'size', 'rate', 'lease_modal'];
  compare_assets_core('.land-compare-checkbox', 'landCompareBtn', 'landClearCompareBtn', 'land', 'landCompareContent', 'landCompareModal', fields);
}

function compare_assets_core(compare_checkboxes, compare_btn, compare_clear_btn, asset_type, compare_content_id, compare_modal_id, fields) {
  const compareCheckboxes = document.querySelectorAll(compare_checkboxes);
  const compareBtn = document.getElementById(compare_btn);
  const compareClearBtn = document.getElementById(compare_clear_btn);

  let selected = [];

  compareCheckboxes.forEach(cb => {
    cb.addEventListener('change', function () {
      const id = parseInt(this.dataset.equipmentId);
      if (this.checked) {
        if (selected.length >= 2) {
          this.checked = false;
          alert('You can only select 2 items for comparison.');
          return;
        }
        selected.push(id);
      } else {
        selected = selected.filter(e => e !== id);
      }
      compareBtn.disabled = selected.length !== 2;
    });
  });

    compareBtn.addEventListener('click', function (event) {
    event.preventDefault();
    
    if (selected.length !== 2) return;

    fetch(`/compare_products/${asset_type}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asset_ids: selected })
    })
    .then(res => res.json())
    .then(data => {
        
        if (data.length < 2) return;
        
        const container = document.getElementById(compare_content_id);
        container.innerHTML = '';

        fields.forEach(field => {
          const row = document.createElement('tr');
          row.classList.add('table');
          row.innerHTML = `
            <th>${field.replace('_', ' ').toUpperCase()}</th>
            <td>${data[0][field] || '-'}</td>
            <td>${data[1][field] || '-'}</td>
          `;
          container.appendChild(row);
        });

        const modal = new bootstrap.Modal(document.getElementById(compare_modal_id));
        modal.show();
    });
    });

        compareClearBtn.addEventListener('click', function (event) {
            event.preventDefault();

            const content = document.getElementById(compare_content_id);
            content.innerHTML = '';
            selected = [];
            compareCheckboxes.forEach(cb => cb.checked = false);
            compareBtn.disabled = true;

        });
}

document.addEventListener('DOMContentLoaded', () => {
    compare_equipment();
    compare_land();

    // Listen for Bootstrap tab click
    const tabLinks = document.querySelectorAll('#search_tab a[data-bs-toggle="pill"]');
        tabLinks.forEach(tabLink => {
            console.log('tabLink', tabLink)
            tabLink.addEventListener('shown.bs.tab', (event) => {
            console.log(event)
            const targetId = event.target.getAttribute('id');

            if (targetId === '#pills-equip-tab') {
                compare_equipment();
            } else if (targetId === '#pills-land-tab') {
                compare_land();
            }
        });
    });
});
