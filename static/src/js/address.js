$(document).ready(function() {
  // Dynamic Upazilla loading
  $('#district').change(function() {
    const url = $('#ClassRegistrationForm').attr('data-upazilla-url');  // Get URL for Upazilla loading
    const districtId = $(this).val();  // Get selected district ID

    $.ajax({
      url: url,
      data: {
        'district_id': districtId
      },
      success: function(data) {
        $('#upazilla').html(data);  // Replace the options in the Upazilla dropdown
        $('#id_union').html('<option value="">Select Union</option>');  // Reset Union dropdown
      }
    });
  });

  // Dynamic Union loading
  $('#upazilla').change(function() {
    const url = $('#ClassRegistrationForm').attr('data-union-url');  // Get URL for Union loading
    const upazillaId = $(this).val();  // Get selected Upazilla ID

    $.ajax({
      url: url,
      data: {
        'upazilla_id': upazillaId
      },
      success: function(data) {
        $('#id_union').html(data);  // Replace the options in the Union dropdown
      }
    });
  });
});



