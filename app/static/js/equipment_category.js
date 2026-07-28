function categoryCascade(categorySelectId, subCategorySelectId, existingCategoryId, existingSubCategoryId, type){

    const categorySelect = document.getElementById(categorySelectId);
    const subCategorySelect = document.getElementById(subCategorySelectId);

    if (type === 'search') { 
        categorySelect.innerHTML = '<option value="0" selected>All Categories</option>';
    } else {
        categorySelect.innerHTML = '<option value="">Select a Category</option>';
    }
    
    
    
    // Populate the initial category dropdown
    fetch('/equipment/categories')
        .then(response => response.json())
        .then(data => {
            data.forEach(category => {
                const option = document.createElement('option');
                option.value = category.category_id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });

            if (existingCategoryId) {
                categorySelect.value = existingCategoryId;
                
            }

            categorySelect.dispatchEvent(new Event('change')); // Trigger change to load subcategories


        });
    
    // Listen for changes on the category dropdown
    categorySelect.addEventListener('change', () => {
        const categoryId = categorySelect.value;
        if(subCategorySelect) {
            subCategorySelect.innerHTML = '<option value="">Select a Sub Category</option>';
        }

        if (categoryId) {
            // Fetch sub-categories based on the selected category ID
            fetch(`/equipment/subcategories/${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    subCategorySelect.innerHTML = '<option value="">Select a Sub Category</option>';
                    data.forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub.subcategory_id;
                        option.textContent = sub.name;
                        subCategorySelect.appendChild(option);
                    });

                    if (existingSubCategoryId && data.some(sub => sub.subcategory_id == existingSubCategoryId)) {
                        subCategorySelect.value = existingSubCategoryId;
                    } else {
                        // Reset selection to placeholder on change by user
                        subCategorySelect.value = "";
                    }

                });
        }
    });

}

document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.edit_equipment_form').forEach(form => {
        const equipmentId = form.dataset.equipmentId;
        const categoryId = parseInt(form.dataset.categoryId, 10);
        const subCategoryId = parseInt(form.dataset.subCategoryId, 10);

        const categorySelectId = 'edit-categories_' + equipmentId;
        const subCategorySelectId = `edit-subcategories_${equipmentId}`;

        categoryCascade(categorySelectId, subCategorySelectId, categoryId, subCategoryId, null)

    });

    document.querySelectorAll('.add_equipment_form').forEach(form => {

        categoryCascade('equipment_category', 'equipment_subcategory', null, null, null)

    });
    
    document.querySelectorAll('.equip_search_form').forEach(form => {

        categoryCascade('search_category', 'search_subcategory', null, null, 'search')

    });

});

