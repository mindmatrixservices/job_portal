
        $(document).ready(function() {
            // Show/hide experience fields based on jobFor selection
            $('input[name="jobfor"]').change(function() {
                if ($(this).val() === 'Experienced') {
                    $('#experienceFields').show();
                    $('#technicalSkills').attr('required', true);
                } else {
                    $('#experienceFields').hide();
                    $('#minExperience, #maxExperience, #technicalSkills').val('');
                    $('#technicalSkills').removeAttr('required');
                }
            });

            // Show/hide government/private fields
            $('input[name="vacancies_for"]').change(function() {
                if ($(this).val() === 'Government') {
                    $('#governmentFields').show();
                    $('#privateFields').hide();
                    $('#min_salary, #max_salary').val('');
                } else {
                    $('#governmentFields').hide();
                    $('#privateFields').show();
                    $('#pay_scale').val('');
                }
            });

            // Show/hide PWD fields
            $('input[name="pwdApplicable"]').change(function() {
                if ($(this).val() === 'Yes') {
                    $('#pwdFields').show();
                    $('#nonPwdFields').hide();
                } else {
                    $('#pwdFields').hide();
                    $('#nonPwdFields').show();
                }
            });

// Show/hide PWD fields based on radio button selection
document.querySelectorAll('input[name="pwdApplicable"]').forEach(radio => {
    radio.addEventListener('change', function() {
        document.getElementById('pwdFields').style.display = 
            this.value === 'Yes' ? 'block' : 'none';
    });
});

// Counter for dynamic tables
let tableCounter = 1;

// Function to add a new complete table
document.getElementById('addPwdRow').addEventListener('click', function() {
    tableCounter++;
    const pwdRows = document.getElementById('pwdRows');
    const newTableDiv = document.createElement('div');
    newTableDiv.className = 'dynamic-row mt-4';
    newTableDiv.innerHTML = `
        <table class="table" style="width:100%">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Number of Vacancies</th>
                    <th>Location<span class="red_hint">*</span></th>
                </tr>
            </thead>                                        
            <tbody>                                        
                <tr>
                    <td><span>Open Category/Unreserved</span></td>
                    <td><input type="text" class="form-control sum_vacancies" name="opencategory_total_vacancy${tableCounter}" id="openCategory_vacancy${tableCounter}" minlength="1" maxlength="2" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                    <td rowspan="9">
                        <select class="form-control" name="category_location${tableCounter}" id="location${tableCounter}" onchange="showInput(this)">
                            <option value=""> Select Location </option>
                            <option value="123">Barpather Dhansiri</option>
                            <option value="93">Barpeta</option>
                            <option value="124">Biswanath Chariali</option>
                            <option value="126">Bokajan</option>                                           
                            <option value="119">Tinsukia</option>
                            <option value="138">Udalguri</option>
                            <option value="other_location">Other Location</option>
                        </select>
                        <div class="col-md-4 pad_lr_0" id="custom_location_container${tableCounter}" style="display: none; margin-top: 10px;">
                            <input type="text" class="form-control" name="custom_location${tableCounter}" id="custom_location${tableCounter}" placeholder="Enter other location">
                        </div>
                    </td>
                    
                </tr>
                <tr>
                    <td><span>OBC</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="obc_total_vacancy${tableCounter}" id="obc_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>Scheduled caste</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="sc_total_vacancy${tableCounter}" id="scheduled_caste_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>Scheduled Tribe</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="st_total_vacancy${tableCounter}" id="scheduled_tribe_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>EWS</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="ews_total_vacancy${tableCounter}" id="ews_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>Ex-Servicemen</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="exservicemen_total_vacancy${tableCounter}" id="exservicemen_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>Persons with disabilities PwD</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="pwd_total_vacancy${tableCounter}" id="pwd_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td><span>Women</span></td>
                    <td><input type="text" class="form-control sum_vacancies" minlength="1" name="women_total_vacancy${tableCounter}" id="women_vacancy${tableCounter}" onkeypress="return event.charCode>=48 && event.charCode<=57" onkeyup="calculateTotal()" placeholder="Number of Vacancies"></td>
                </tr>
                <tr>
                    <td colspan="3" class="text-center">
                        <button type="button" class=" btn btn-danger btn-sm remove-table"><i class="fas fa-trash"></i> Remove </button>
                    </td>
                </tr>                                      
            </tbody>
        </table>
    `;
    
    pwdRows.appendChild(newTableDiv);
    
    // Recalculate totals after adding new table
    calculateTotal();
});

// Remove table functionality using event delegation
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('remove-table') || e.target.closest('.remove-table')) {
        const button = e.target.classList.contains('remove-table') ? 
                      e.target : e.target.closest('.remove-table');
        const tableDiv = button.closest('.dynamic-row');
        
        // Don't allow removing the first table
        if (tableDiv && !tableDiv.previousElementSibling) {
            alert("You cannot remove the first table.");
            return;
        }
        
        if (tableDiv) {
            tableDiv.remove();
            calculateTotal();
        }
    }
});

// Global showInput function that works with all tables
function showInput(selectElement) {
    const rowNumber = selectElement.id.replace('location', '');
    const customLocationContainer = document.getElementById(`custom_location_container${rowNumber}`);
    
    if (customLocationContainer) {
        const selectedText = selectElement.options[selectElement.selectedIndex].text;
        
        if (selectedText.trim().toLowerCase() === 'other location') {
            customLocationContainer.style.display = 'block';
        } else {
            customLocationContainer.style.display = 'none';
            document.getElementById(`custom_location${rowNumber}`).value = '';
        }
    }
}


            // Add dynamic location row
            // Counter for location rows
let locationRowCounter = 1;

// Function to add new location row
document.getElementById('addLocationRow').addEventListener('click', function() {
    locationRowCounter++;
    const locationRows = document.querySelector('#locationRows tbody');
    
    const newRow = document.createElement('tr');
    newRow.className = 'dynamic-row';
    newRow.innerHTML = `
        <td>
            <select class="form-select" name="location[]">
                <option value="Delhi">Delhi</option>
                <option value="Mumbai">Mumbai</option>
                <option value="Bangalore">Bangalore</option>
                <option value="Hyderabad">Hyderabad</option>
                <option value="Chennai">Chennai</option>
                <option value="Kolkata">Kolkata</option>
            </select>
        </td>
        <td>
            <input type="number" class="form-control" name="locationPosts[]" min="0">
        </td>
        <td class="text-center align-middle">
            <button type="button" class="btn btn-danger btn-sm remove-location-row">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    
    locationRows.appendChild(newRow);
});

// Remove location row functionality
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('remove-location-row') || 
        e.target.closest('.remove-location-row')) {
        e.preventDefault();
        const button = e.target.classList.contains('remove-location-row') ? 
                      e.target : e.target.closest('.remove-location-row');
        const row = button.closest('tr');
        const tbody = row.closest('tbody');
        const allRows = tbody.querySelectorAll('tr');
        
        // Check if this is the last removable row (2nd row or later)
        if (allRows.length <= 1) {
            // Create and show a temporary warning message
            const warning = document.createElement('div');
            warning.className = 'alert alert-warning position-fixed top-0 start-50 translate-middle-x mt-2';
            warning.style.zIndex = '1060';
            warning.style.minWidth = '300px';
            warning.textContent = 'You must keep at least one location';
            document.body.appendChild(warning);
            
            // Remove after 2 seconds
            setTimeout(() => warning.remove(), 2000);
            return;
        }
        
        // Only allow removal if it's not the first row and there are other rows
        if (row && row.rowIndex > 0) 
            {row.remove();
        }
    }
});

            // Show/hide job type specific fields
            $('input[name="job_posted_for"]').change(function() {
                if ($(this).val() === 'Open Job') {
                    $('#openJobFields').show();
                } else {
                    $('#openJobFields').hide();
                    $('#postValidity, #postRequestedOn, #message').val('');
                }
            });

            // Form validation
            $('#jobPostingForm').submit(function(e) {
                // You can add additional validation here if needed
                console.log('Form submitted');
                // e.preventDefault(); // Uncomment to prevent actual submission for demo
            });
        });



        $(document).ready(function() {
            // Handle "Same as Indenting Officer" checkbox
            $('#sameAsIndentingOfficer').change(function() {
                if ($(this).is(':checked')) {
                    // Copy values from Approching Officer to Indenting Officer
                    $('#indentingOfficerName').val($('#approchingOfficerName').val());
                    $('#indentingOfficerDesignation').val($('#approchingOfficerDesignation').val());
                    $('#indentingOfficerEmail').val($('#approchingOfficerEmail').val());
                    
                    // Disable the Indenting Officer fields
                    $('#indentingOfficerName, #indentingOfficerDesignation, #indentingOfficerEmail').prop('disabled', true);
                } else {
                    // Clear and enable the Indenting Officer fields
                    $('#indentingOfficerName, #indentingOfficerDesignation, #indentingOfficerEmail').val('').prop('disabled', false);
                }
            });
            
            // Update Indenting Officer fields when Approching Officer fields change (if checkbox is checked)
            $('#approchingOfficerName, #approchingOfficerDesignation, #approchingOfficerEmail').on('input', function() {
                if ($('#sameAsIndentingOfficer').is(':checked')) {
                    $('#indentingOfficerName').val($('#approchingOfficerName').val());
                    $('#indentingOfficerDesignation').val($('#approchingOfficerDesignation').val());
                    $('#indentingOfficerEmail').val($('#approchingOfficerEmail').val());
                }
            });
        });

