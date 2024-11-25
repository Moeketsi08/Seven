$(document).ready(function(){
    $('#id_district').change(function(){
        var url = $('#ClassRegistrationForm').attr("data-upazilla-url");
        var districtId = $(this).val();
        $.ajax({
            url: url,
            data: {
                'district_id': districtId
            },
            success: function(data) {
                $("#id_upazilla").html(data);
            }
        });
    });

    $('#id_upazilla').change(function(){
        var url = $('#ClassRegistrationForm').attr("data-union-url");
        var upazillaId = $(this).val();
        $.ajax({
            url: url,
            data: {
                'upazilla_id': upazillaId
            },
            success: function(data) {
                $("#id_union").html(data);
            }
        });
    });
});

