class HashIdFieldAdminMixin:
    def _decode_id(self, model, object_id):
        obj = model(id=object_id)
        return "{}".format(obj.id.id)  # Return the integer value of the Hashid as a string

    def history_view(self, request, object_id, extra_context=None):
        decoded_id = self._decode_id(self.model, object_id)

        return super().history_view(request, decoded_id, extra_context=extra_context)

    def history_form_view(self, request, object_id, version_id):
        decoded_id = self._decode_id(self.model, object_id)

        return super().history_form_view(request, decoded_id, version_id)
