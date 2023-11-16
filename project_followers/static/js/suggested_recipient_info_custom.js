odoo.define('project_followers.suggested_recipient_info_custom', function (require) {
    'use strict';

    const SuggestedRecipientInfo = require('mail.suggested_recipient_info');

    SuggestedRecipientInfo.include({
        /**
         * @private
         * @returns {boolean}
         */
        _computeIsSelected: function () {
            // Votre code de surcharge ici
            // N'oubliez pas d'appeler la fonction d'origine si nécessaire
            return this.partner ? this.isSelected : false;
        },
    });
});