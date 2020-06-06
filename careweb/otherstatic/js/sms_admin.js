window.onload = function () {
    const $ = jQuery;
    $(document).ready(function () {
        const fPlan = $('.field-plan');
        const fRecipients = $('.field-recipients');
        const cCategory = $('#id_category');
        cCategory.on('change', function () {
            const val = $(this).val();
            categoryChanged(val);
        });

        function categoryChanged(val) {
            if (val === "P") {
                fPlan.show();
                fRecipients.hide();
            } else if (val === "C") {
                fPlan.hide();
                fRecipients.show();
            } else {
                fPlan.hide();
                fRecipients.hide();
            }
        }
        categoryChanged(cCategory.val());
    });
};

