window.onload = function () {
    const $ = jQuery;
    $('#id_lga').val('');
    $(document).ready(function () {
        const lga_select = $("#id_lga");

        lga_select.change(function () {
            const val = lga_select.val();
            $.ajax({
                url: "/client/lga/pcps",
                type: "GET",
                data: {lga: val},
                dataType: "json",
                success: function (data) {
                    const pcp_select = $('#id_pcp');
                    const pcps = data.pcps;

                    let options = '<option value="">---------</option>';
                    for (let index in pcps) {
                        if (pcps.hasOwnProperty(index)) {
                            const row = pcps[index];
                            options += "<option value='" + row.id + "'>" + row.text + "</option>";
                        }
                    }
                    pcp_select.html(options);
                },
                error: function (xhr) {
                    console.log(xhr.responseText);
                }
            })
        });
    });
};

